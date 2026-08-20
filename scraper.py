from playwright.sync_api import sync_playwright
import pandas as pd
import os
import re

URL = "https://www.nykaa.com/deals-of-the-day/c/52098"
OUTPUT_FILE = "data/nykaa_products.csv"


def clean_price(value):
    """Extract a numeric price from text such as ₹999 or ₹1,299."""
    if not value:
        return ""

    match = re.search(r"₹\s*([\d,]+)", value)

    if match:
        return match.group(1).replace(",", "")

    return ""


def clean_discount(value):
    """Extract discount percentage."""
    if not value:
        return ""

    match = re.search(r"(\d+)\s*%", value)

    if match:
        return match.group(1) + "%"

    return ""


def get_product_data(card):
    """Extract information from one possible product card."""

    try:
        text = card.inner_text().strip()

        if not text:
            return None

        # Find all prices in the card
        prices = re.findall(r"₹\s*[\d,]+", text)

        # Find discount
        discount_match = re.search(
            r"(\d+)\s*%\s*(?:OFF|off|Off)?",
            text
        )

        discount = ""

        if discount_match:
            discount = discount_match.group(1) + "%"

        # We need at least two prices to consider this a discounted product
        if len(prices) < 2:
            return None

        original_price = clean_price(prices[0])
        discounted_price = clean_price(prices[1])

        # Get individual text lines
        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        # Remove lines that are obviously prices/discounts
        name_lines = []

        for line in lines:

            if "₹" in line:
                continue

            if "%" in line:
                continue

            if "OFF" in line.upper():
                continue

            name_lines.append(line)

        # Choose the longest useful text as product name
        product_name = ""

        if name_lines:
            product_name = max(
                name_lines,
                key=len
            )

        # Ignore navigation/filter text
        unwanted = [
            "Deals of the Day",
            "All Products",
            "Sort By",
            "Popularity",
            "Brand",
            "Price",
            "Category",
            "Discount",
            "Avg Customer Rating",
            "Preference"
        ]

        if product_name in unwanted:
            return None

        if len(product_name) < 5:
            return None

        return {
            "Product Name": product_name,
            "Original Price": original_price,
            "Discounted Price": discounted_price,
            "Discount": discount
        }

    except Exception:
        return None


def main():

    print("Starting Nykaa scraper...")

    products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 1000
            }
        )

        print("Opening Nykaa...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Waiting for products to load...")

        page.wait_for_timeout(10000)

        # Scroll several times to load dynamically loaded products
        for i in range(10):

            print(
                f"Loading products... {i + 1}/10"
            )

            page.mouse.wheel(
                0,
                1500
            )

            page.wait_for_timeout(2000)

        print("Searching for product cards...")

        # Get all elements that contain ₹
        elements = page.locator(
            "text=/₹/"
        )

        print(
            "Price-containing elements:",
            elements.count()
        )

        # Examine elements and their parents
        for i in range(
            min(elements.count(), 500)
        ):

            try:

                element = elements.nth(i)

                # Move upwards through parents
                card = element

                for level in range(6):

                    card = card.locator("..")

                    text = card.inner_text().strip()

                    # A reasonable product card usually has
                    # multiple lines and multiple prices
                    price_count = len(
                        re.findall(
                            r"₹\s*[\d,]+",
                            text
                        )
                    )

                    if price_count >= 2:

                        product = get_product_data(
                            card
                        )

                        if product:
                            products.append(product)

                        break

            except Exception:
                continue

        browser.close()

    # Remove duplicates
    unique_products = []
    seen = set()

    for product in products:

        key = (
            product["Product Name"],
            product["Original Price"],
            product["Discounted Price"]
        )

        if key not in seen:

            seen.add(key)

            unique_products.append(
                product
            )

    # Create data directory
    os.makedirs(
        "data",
        exist_ok=True
    )

    # Create DataFrame
    df = pd.DataFrame(
        unique_products
    )

    # Save CSV
    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("=" * 50)
    print("SCRAPING COMPLETED")
    print("=" * 50)
    print(
        "Products found:",
        len(df)
    )
    print(
        "CSV saved to:",
        OUTPUT_FILE
    )
    print("=" * 50)

    if len(df) > 0:

        print()
        print("First 10 products:")
        print(
            df.head(10).to_string(
                index=False
            )
        )

    else:

        print()
        print(
            "No products were detected."
        )

        print(
            "Nykaa may have changed its page structure."
        )


if __name__ == "__main__":
    main()