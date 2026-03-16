import httpx
from bs4 import BeautifulSoup

from app.domains.news.application.port.article_content_provider import (
    ArticleContentProvider,
)


class ArticleContentScraper(ArticleContentProvider):
    """기사 링크에 접근하여 본문 텍스트를 추출하는 Adapter"""

    async def fetch_content(self, url: str) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        try:
            async with httpx.AsyncClient(
                timeout=15.0, follow_redirects=True
            ) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # 불필요한 태그 제거
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()

            # <article> 태그 우선, 없으면 <body> 전체
            article_tag = soup.find("article")
            target = article_tag if article_tag else soup.find("body")

            if target is None:
                return ""

            paragraphs = target.find_all("p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            return text if text else target.get_text(separator="\n", strip=True)

        except Exception:
            return ""
