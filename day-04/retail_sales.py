# ============================================================
# RETAIL SALES ANALYSIS SYSTEM
# Analyse retail_sales.xlsx using Python and openpyxl
# ============================================================

from openpyxl import load_workbook

INPUT_FILE = "retail_sales.xlsx"
REPORT_FILE = "sales_report.txt"
ERROR_FILE = "invalid_records.log"
LOW_STOCK_LIMIT = 10

sales = []
invalid_records = []
category_data = {}


# 1. LOAD THE EXCEL WORKBOOK
def load_sales_file():
    try:
        workbook = load_workbook(INPUT_FILE, data_only=True)
        return workbook, workbook.active
    except FileNotFoundError:
        print("ERROR: retail_sales.xlsx was not found.")
    except Exception as error:
        print("ERROR loading workbook:", error)
    return None, None


# 2. READ ROWS AND 3. VALIDATE REQUIRED VALUES
def read_transactions(sheet):
    headers = [
        str(cell.value).strip().lower() if cell.value is not None else ""
        for cell in sheet[1]
    ]

    required_fields = [
        "sale id", "product", "category", "quantity", "price", "stock"
    ]

    positions = {}
    for field in required_fields:
        if field not in headers:
            raise ValueError("Missing Excel column: " + field)
        positions[field] = headers.index(field)

    for row_number, row in enumerate(
        sheet.iter_rows(min_row=2, values_only=True), start=2
    ):
        if all(value is None for value in row):
            continue

        sale_id = row[positions["sale id"]]
        product = row[positions["product"]]
        category = row[positions["category"]]
        quantity = row[positions["quantity"]]
        price = row[positions["price"]]
        stock = row[positions["stock"]]

        reasons = []

        if sale_id is None or str(sale_id).strip() == "":
            reasons.append("Missing sale ID")
        if product is None or str(product).strip() == "":
            reasons.append("Missing product")
        if category is None or str(category).strip() == "":
            reasons.append("Missing category")

        try:
            quantity = float(quantity)
            if quantity <= 0:
                reasons.append("Quantity must be greater than zero")
        except (ValueError, TypeError):
            quantity = 0
            reasons.append("Invalid quantity")

        try:
            price = float(price)
            if price < 0:
                reasons.append("Price cannot be negative")
        except (ValueError, TypeError):
            price = 0
            reasons.append("Invalid price")

        try:
            stock = float(stock)
            if stock < 0:
                reasons.append("Stock cannot be negative")
        except (ValueError, TypeError):
            stock = 0
            reasons.append("Invalid stock")

        if reasons:
            invalid_records.append(
                "Excel row " + str(row_number) + " | " +
                ", ".join(reasons) + " | " + str(row)
            )
        else:
            sales.append({
                "sale_id": str(sale_id).strip(),
                "product": str(product).strip(),
                "category": str(category).strip(),
                "quantity": quantity,
                "price": price,
                "stock": stock
            })


# CHECK DUPLICATE SALE IDs
def check_duplicates():
    unique_sales = []
    seen_ids = set()

    for record in sales:
        sale_id = record["sale_id"]
        if sale_id in seen_ids:
            invalid_records.append("Duplicate sale ID: " + sale_id)
        else:
            seen_ids.add(sale_id)
            unique_sales.append(record)

    sales.clear()
    for record in unique_sales:
        sales.append(record)


# 4. CALCULATE REVENUE USING MULTIPLICATION AND LOOPS
def calculate_revenue():
    total_revenue = 0

    for record in sales:
        revenue = record["quantity"] * record["price"]
        record["revenue"] = revenue
        total_revenue = total_revenue + revenue

    return total_revenue


# 5. AGGREGATE REVENUE BY CATEGORY
def analyse_categories():
    for record in sales:
        category = record["category"]

        if category not in category_data:
            category_data[category] = {
                "revenue": 0,
                "quantity": 0,
                "transactions": 0
            }

        category_data[category]["revenue"] += record["revenue"]
        category_data[category]["quantity"] += record["quantity"]
        category_data[category]["transactions"] += 1


# MANUALLY RANK TOP FIVE CATEGORIES
def rank_categories():
    remaining = []

    for category in category_data:
        remaining.append({
            "category": category,
            "revenue": category_data[category]["revenue"]
        })

    ranked = []
    for position in range(5):
        if len(remaining) == 0:
            break

        highest_index = 0
        for index in range(1, len(remaining)):
            if remaining[index]["revenue"] > remaining[highest_index]["revenue"]:
                highest_index = index

        ranked.append(remaining.pop(highest_index))

    return ranked


# 6. MANUALLY RANK TOP TEN TRANSACTIONS
def rank_transactions():
    remaining = []
    for record in sales:
        remaining.append(record)

    top_transactions = []
    for position in range(10):
        if len(remaining) == 0:
            break

        highest_index = 0
        for index in range(1, len(remaining)):
            if remaining[index]["revenue"] > remaining[highest_index]["revenue"]:
                highest_index = index

        top_transactions.append(remaining.pop(highest_index))

    return top_transactions


# IDENTIFY LOW-STOCK PRODUCTS
def identify_low_stock():
    low_stock_products = []

    for record in sales:
        if record["stock"] <= LOW_STOCK_LIMIT:
            low_stock_products.append(record)

    return low_stock_products


# 7. EXPORT THE SALES REPORT
def create_sales_report(total_revenue, ranked_categories,
                        top_transactions, low_stock_products):
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("RETAIL SALES ANALYSIS REPORT\n")
        file.write("=" * 45 + "\n\n")
        file.write("Valid transactions: " + str(len(sales)) + "\n")
        file.write("Invalid records: " + str(len(invalid_records)) + "\n")
        file.write("Total revenue: R" + format(total_revenue, ".2f") + "\n\n")

        file.write("TOP FIVE PRODUCT CATEGORIES\n")
        rank = 1
        for item in ranked_categories:
            file.write(
                str(rank) + ". " + item["category"] +
                " | Revenue: R" + format(item["revenue"], ".2f") + "\n"
            )
            rank += 1

        file.write("\nTOP TEN TRANSACTIONS\n")
        rank = 1
        for record in top_transactions:
            file.write(
                str(rank) + ". Sale ID: " + record["sale_id"] +
                " | Product: " + record["product"] +
                " | Revenue: R" + format(record["revenue"], ".2f") + "\n"
            )
            rank += 1

        file.write("\nLOW STOCK PRODUCTS (10 OR FEWER)\n")
        for record in low_stock_products:
            file.write(
                record["product"] + " | Category: " + record["category"] +
                " | Stock: " + str(record["stock"]) + "\n"
            )


# CREATE THE INVALID-RECORD LOG
def create_error_log():
    with open(ERROR_FILE, "w", encoding="utf-8") as file:
        file.write("RETAIL SALES - INVALID RECORD LOG\n")
        file.write("=" * 45 + "\n\n")
        for error in invalid_records:
            file.write(error + "\n")
        file.write("\nTotal invalid records: " + str(len(invalid_records)))


# DISPLAY RESULTS IN THONNY SHELL
def display_results(total_revenue, ranked_categories,
                    top_transactions, low_stock_products):
    print("\nRETAIL SALES ANALYSIS")
    print("Valid transactions:", len(sales))
    print("Invalid records:", len(invalid_records))
    print("Total revenue: R" + format(total_revenue, ".2f"))

    print("\nTOP FIVE CATEGORIES")
    rank = 1
    for item in ranked_categories:
        print(rank, item["category"], "R" + format(item["revenue"], ".2f"))
        rank += 1

    print("\nTOP TEN TRANSACTIONS")
    rank = 1
    for record in top_transactions:
        print(rank, record["sale_id"], record["product"],
              "R" + format(record["revenue"], ".2f"))
        rank += 1

    print("\nLow-stock records:", len(low_stock_products))
    print("Report saved as:", REPORT_FILE)
    print("Error log saved as:", ERROR_FILE)


# MAIN PROGRAM
def main():
    print("Starting Retail Sales Analysis System...")

    workbook, sheet = load_sales_file()
    if sheet is None:
        return

    try:
        read_transactions(sheet)
        check_duplicates()
        total_revenue = calculate_revenue()
        analyse_categories()
        ranked_categories = rank_categories()
        top_transactions = rank_transactions()
        low_stock_products = identify_low_stock()

        create_sales_report(
            total_revenue, ranked_categories,
            top_transactions, low_stock_products
        )
        create_error_log()
        display_results(
            total_revenue, ranked_categories,
            top_transactions, low_stock_products
        )
        print("\nProgram completed successfully.")

    except (ValueError, IndexError) as error:
        print("Processing error:", error)

    finally:
        workbook.close()


if __name__ == "__main__":
    main()
