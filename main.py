import pandas as pd
from fpdf import FPDF

df = pd.read_csv("articles.csv", dtype={"id": str})


class Article:
    def __init__(self, article_id):
        self.article_id = article_id
        self.article_name = df.loc[df["id"] == self.article_id, "name"].squeeze()
        self.price = df.loc[df["id"] == self.article_id, "price"].squeeze()

    def available(self):
        """Checks to see if the item is in stock"""
        in_stock = df.loc[df["id"] == self.article_id, "in stock"].squeeze()
        return in_stock

    def purchase(self):
        """Purchase an item that is available"""
        df.loc[df["id"] == self.article_id, "in stock"] -= 1
        df.to_csv("articles.csv", index=False)


class Receipt:
    def __init__(self, article):
        self.article = article

    def generate_pdf(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article_name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.price}", ln=1)

        pdf.output("receipt.pdf")


if __name__ == "__main__":
    print(df)
    article_id = input("Choose an article to buy: ")
    article = Article(article_id=article_id)

    if article.available():
        article.purchase()
        print(f"Thank you for you purchase. You soon will have a receipt.")
        receipt = Receipt(article_id)
        receipt.generate_pdf()
    else:
        print("The article is not available.")
