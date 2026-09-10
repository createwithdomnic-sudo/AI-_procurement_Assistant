from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)


# =====================================================
# LOAD PURCHASE ORDERS
# =====================================================

def load_purchase_orders():

    with open("purchase_orders.json", "r") as file:
        return json.load(file)


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# GET ALL PURCHASE ORDERS
# =====================================================

@app.route("/api/purchase-orders")
def get_purchase_orders():

    orders = load_purchase_orders()

    return jsonify(orders)


# =====================================================
# GET OVERDUE ORDERS
# =====================================================

@app.route("/api/overdue-orders")
def get_overdue_orders():

    orders = load_purchase_orders()

    overdue_orders = [
        order
        for order in orders
        if order["status"].lower() == "overdue"
    ]

    return jsonify(overdue_orders)


# =====================================================
# RISK CALCULATION
# =====================================================

def calculate_risk(order):

    amount = order["amount"]

    status = order["status"].lower()

    if status == "overdue":

        if amount >= 200000:
            return "HIGH"

        elif amount >= 100000:
            return "MEDIUM"

        else:
            return "LOW"

    return "LOW"


# =====================================================
# RISK ANALYSIS API
# =====================================================

@app.route("/api/risk-analysis")
def risk_analysis():

    orders = load_purchase_orders()

    results = []

    for order in orders:

        risk = calculate_risk(order)

        results.append({
            "po_id": order["po_id"],
            "supplier": order["supplier"],
            "amount": order["amount"],
            "delivery_date": order["delivery_date"],
            "status": order["status"],
            "risk": risk
        })

    return jsonify(results)


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

@app.route("/api/summary")
def summary():

    orders = load_purchase_orders()

    total_orders = len(orders)

    overdue_orders = [
        order
        for order in orders
        if order["status"].lower() == "overdue"
    ]

    total_value = sum(
        order["amount"]
        for order in orders
    )

    overdue_value = sum(
        order["amount"]
        for order in overdue_orders
    )

    high_risk_orders = sum(
        1
        for order in orders
        if calculate_risk(order) == "HIGH"
    )

    return jsonify({

        "total_orders": total_orders,

        "overdue_orders": len(overdue_orders),

        "total_value": total_value,

        "overdue_value": overdue_value,

        "high_risk_orders": high_risk_orders

    })


# =====================================================
# PROCUREMENT ASSISTANT
# =====================================================

@app.route("/api/ask", methods=["POST"])
def ask_assistant():

    data = request.get_json()

    question = data.get("question", "").lower().strip()

    orders = load_purchase_orders()


    # -------------------------------------------------
    # EMPTY QUESTION
    # -------------------------------------------------

    if not question:

        return jsonify({
            "answer": "Please enter a procurement question."
        })


    # -------------------------------------------------
    # OVERDUE QUESTIONS
    # -------------------------------------------------

    if "overdue" in question:

        overdue = [
            order
            for order in orders
            if order["status"].lower() == "overdue"
        ]

        if not overdue:

            answer = "There are no overdue purchase orders."

        else:

            answer = "Overdue purchase orders:\n\n"

            for order in overdue:

                answer += (
                    f"PO {order['po_id']} - "
                    f"{order['supplier']} - "
                    f"₹{order['amount']:,} - "
                    f"Delivery: {order['delivery_date']}\n"
                )

        return jsonify({
            "answer": answer
        })


    # -------------------------------------------------
    # HIGH RISK QUESTIONS
    # -------------------------------------------------

    if "high risk" in question or "high-risk" in question:

        high_risk = [
            order
            for order in orders
            if calculate_risk(order) == "HIGH"
        ]

        if not high_risk:

            answer = "There are no high-risk purchase orders."

        else:

            answer = "High-risk purchase orders:\n\n"

            for order in high_risk:

                answer += (
                    f"PO {order['po_id']} - "
                    f"{order['supplier']} - "
                    f"₹{order['amount']:,}\n"
                )

        return jsonify({
            "answer": answer
        })


    # -------------------------------------------------
    # SUPPLIER QUESTIONS
    # -------------------------------------------------

    if "supplier" in question:

        suppliers = sorted(
            set(
                order["supplier"]
                for order in orders
            )
        )

        answer = "Suppliers:\n\n"

        for supplier in suppliers:

            answer += f"• {supplier}\n"

        return jsonify({
            "answer": answer
        })


    # -------------------------------------------------
    # TOTAL VALUE QUESTIONS
    # -------------------------------------------------

    if "total value" in question or "total amount" in question:

        total = sum(
            order["amount"]
            for order in orders
        )

        answer = (
            f"Total purchase order value is "
            f"₹{total:,}."
        )

        return jsonify({
            "answer": answer
        })


    # -------------------------------------------------
    # TOTAL ORDER QUESTIONS
    # -------------------------------------------------

    if "how many orders" in question or "total orders" in question:

        answer = (
            f"There are {len(orders)} "
            f"purchase orders."
        )

        return jsonify({
            "answer": answer
        })


    # -------------------------------------------------
    # SPECIFIC PO SEARCH
    # -------------------------------------------------

    for order in orders:

        if order["po_id"] in question:

            risk = calculate_risk(order)

            answer = (
                f"PO {order['po_id']}\n"
                f"Supplier: {order['supplier']}\n"
                f"Amount: ₹{order['amount']:,}\n"
                f"Delivery Date: {order['delivery_date']}\n"
                f"Status: {order['status']}\n"
                f"Risk: {risk}"
            )

            return jsonify({
                "answer": answer
            })


    # -------------------------------------------------
    # DEFAULT RESPONSE
    # -------------------------------------------------

    answer = (
        "I can help you with:\n\n"
        "• Overdue purchase orders\n"
        "• High-risk orders\n"
        "• Suppliers\n"
        "• Total order value\n"
        "• Purchase order details\n\n"
        "Try asking: "
        "\"Which orders are overdue?\""
    )

    return jsonify({
        "answer": answer
    })


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )