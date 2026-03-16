from abc import ABC, abstractmethod


class ArticleContentProvider(ABC):

    @abstractmethod
    async def fetch_content(self, url: str) -> str:
        """기사 링크에 접근하여 본문 내용을 추출한다."""
        pass
