from threading import Lock

import torch
from transformers import AutoModel, AutoTokenizer


def mean_pooling(token_embeddings, mask):
    token_embeddings = token_embeddings.masked_fill(~mask[..., None].bool(), 0.0)
    return token_embeddings.sum(dim=1) / mask.sum(dim=1)[..., None]


class ContrieverRetriever:
    def __init__(self, model_path, device="cuda"):
        self.device = device
        self.model = AutoModel.from_pretrained(model_path).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.lock = Lock()

    def embed(self, sentences, batch_size=32):
        all_embeddings = []
        for start in range(0, len(sentences), batch_size):
            batch = sentences[start:start + batch_size]
            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                return_tensors="pt",
            ).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs[0], inputs["attention_mask"])
            all_embeddings.append(embeddings.cpu())
        return torch.vstack(all_embeddings)

    def retrieve(self, query, embeddings, k=2):
        with self.lock:
            inputs = self.tokenizer(
                [query],
                padding=True,
                truncation=True,
                return_tensors="pt",
            ).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                query_embedding = mean_pooling(
                    outputs[0],
                    inputs["attention_mask"],
                ).cpu()

        similarity = (query_embedding @ embeddings.T)[0]
        nearest = similarity.topk(min(len(embeddings), k), largest=True)
        return nearest.indices, similarity
