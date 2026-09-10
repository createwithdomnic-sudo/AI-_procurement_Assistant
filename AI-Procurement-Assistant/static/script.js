// ==================================================
// LOAD DASHBOARD SUMMARY
// ==================================================

async function loadSummary() {

    try {

        const response =
            await fetch("/api/summary");

        const data =
            await response.json();


        document.getElementById("totalOrders")
            .innerText =
            data.total_orders;


        document.getElementById("overdueOrders")
            .innerText =
            data.overdue_orders;


        document.getElementById("totalValue")
            .innerText =
            "₹" +
            data.total_value.toLocaleString("en-IN");


        document.getElementById("highRiskOrders")
            .innerText =
            data.high_risk_orders;

    }

    catch (error) {

        console.error(
            "Summary error:",
            error
        );

    }

}


// ==================================================
// LOAD PURCHASE ORDERS
// ==================================================

async function loadOrders() {

    try {

        const response =
            await fetch("/api/purchase-orders");

        const orders =
            await response.json();


        displayOrders(orders);

    }

    catch (error) {

        console.error(
            "Orders error:",
            error
        );

    }

}


// ==================================================
// LOAD RISK ANALYSIS
// ==================================================

async function loadRiskAnalysis() {

    try {

        const response =
            await fetch("/api/risk-analysis");

        const orders =
            await response.json();


        displayOrders(orders);

    }

    catch (error) {

        console.error(
            "Risk error:",
            error
        );

    }

}


// ==================================================
// DISPLAY ORDERS
// ==================================================

function displayOrders(orders) {

    let html = `

        <table>

            <thead>

                <tr>

                    <th>PO ID</th>

                    <th>Supplier</th>

                    <th>Amount</th>

                    <th>Delivery Date</th>

                    <th>Status</th>

                    <th>Risk</th>

                </tr>

            </thead>

            <tbody>

    `;


    orders.forEach(order => {

        html += `

            <tr>

                <td>
                    ${order.po_id}
                </td>

                <td>
                    ${order.supplier}
                </td>

                <td>
                    ₹${order.amount.toLocaleString("en-IN")}
                </td>

                <td>
                    ${order.delivery_date}
                </td>

                <td>
                    ${order.status}
                </td>

                <td>
                    ${order.risk || "-"}
                </td>

            </tr>

        `;

    });


    html += `

            </tbody>

        </table>

    `;


    document.getElementById("orders")
        .innerHTML = html;

}


// ==================================================
// ASK PROCUREMENT ASSISTANT
// ==================================================

async function askAssistant() {

    const input =
        document.getElementById("question");


    const answerBox =
        document.getElementById("answer");


    const question =
        input.value.trim();


    if (question === "") {

        answerBox.innerText =
            "Please enter a question.";

        return;

    }


    answerBox.innerText =
        "Analyzing procurement data...";


    try {

        const response =
            await fetch("/api/ask", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    question: question

                })

            });


        const data =
            await response.json();


        answerBox.innerText =
            data.answer;

    }

    catch (error) {

        console.error(
            "Assistant error:",
            error
        );


        answerBox.innerText =
            "Unable to connect to the assistant.";

    }

}


// ==================================================
// ENTER KEY
// ==================================================

document
    .getElementById("question")
    .addEventListener(
        "keypress",
        function(event) {

            if (event.key === "Enter") {

                askAssistant();

            }

        }
    );


// ==================================================
// INITIAL DASHBOARD LOAD
// ==================================================

loadSummary();