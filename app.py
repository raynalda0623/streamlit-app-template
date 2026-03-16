import streamlit as st

#st.set_page_config(page_title="Smart Coffee Kiosk Application")
st.title("Smart Coffee Kiosk Application")
st.write("This application allows customers to place, update, and cancel coffee orders.")
st.divider()

#I need a list of orders. #Each order will be a dictionary with these fields.
#  When someone adds a new order, I append a new dictionary to the list. Loading orders.
orders = [
    {"id": "1", "customer_name": "Raynalda", "coffee_type": "Latte", "size": "Medium"},
    {"id": "2", "customer_name": "Ketsia", "coffee_type": "Espresso", "size": "Small"},
    {"id": "3", "customer_name": "Kejae", "coffee_type": "Cappuccino", "size": "Large"},
    {"id": "4", "customer_name": "Desiree", "coffee_type": "Americano", "size": "Medium"},
]

# Step 2: Make sure there is a place to store coffee orders
if "orders" not in st.session_state:
    st.session_state["orders"] = []

# Step 3: Create four tabs for CRUD operations
tab1, tab2, tab3, tab4 = st.tabs(["View Orders", "Add Order", "Update Order", "Cancel Order"]) 

from pathlib import Path
import json

json_path = Path("orders.json")
if json_path.exists():
    with open(json_path, "r") as f:
        st.session_state["orders"] = json.load(f)

#Now I need to implement the functionality for each tab.
with tab2: 
    st.header("Add a New Coffee Order")
    customer_name = st.text_input("Customer Name", placeholder="Enter customer's name")
    coffee_type = st.selectbox(
    "Coffee Type",
    ["Latte", "Espresso", "Cappuccino", "Americano"],
    key="add_coffee"
)

    size = st.selectbox("Size", ["Small", "Medium", "Large"])
    
    st.divider()

btn_save = st.button("Save Order")  
if btn_save:
        if not customer_name:
            st.warning("Please enter the customer name!")  
        else:
            # Create a new order dictionary
            new_order = {
                "id": str(len(st.session_state["orders"]) + 1),  # ID generation
                "customer_name": customer_name,
                "coffee_type": coffee_type,
                "size": size
            }
            st.session_state["orders"].append(new_order)
            with open(json_path, "w") as f:
                json.dump(st.session_state["orders"], f)
            st.success("Order added successfully!")

with tab1: 
    st.header("View Orders")
    st.subheader(f"Total Orders: {len(st.session_state['orders'])}")

    # Option to choose between viewing all orders or searching by customer name
    option = st.radio("View/Search", ["View All", "Search"], horizontal=True)

    if option == "View All":
        # Show all orders in a table
        st.dataframe(st.session_state["orders"])

    else:
        # Search by customer name
        # Create a list of all customer names from the orders
        customer_names = [order["customer_name"] for order in st.session_state["orders"]]

        if not customer_names:
            # If there are no orders, show a warning
            st.warning("No orders found!")
        else:
            # Select a customer from the list
            selected_customer = st.selectbox("Select Customer", customer_names)
            
            # Loop through orders to find the one that matches the selected customer
            for order in st.session_state["orders"]:
                if order["customer_name"] == selected_customer:
                    # Show the order details inside an expander
                    st.expander("Order Details", expanded=True)
                    st.markdown(f"*Order ID:* {order['id']}")  # Show order ID
                    st.markdown(f"*Customer Name:* {order['customer_name']}")  # Show customer name
                    st.markdown(f"*Coffee Type:* {order['coffee_type']}")  # Show coffee type
                    st.markdown(f"*Size:* {order['size']}")  # Show coffee size
                    break  # Stop looping once we find the order

with tab3:
    st.header("Update an Order")

    #I'm creating a list of customer names from existing orders
    order_customers = [order["customer_name"] for order in st.session_state["orders"]]

    if not order_customers:
        # If no orders exist, show a warning
        st.warning("No orders available to update!")
    else:
        # Then, let the user select which order to update
        selected_customer = st.selectbox("Select Customer to Update", order_customers, key="update_customer")

        #Finding the selected order in the list
        selected_order = {}
        for order in st.session_state["orders"]:
            if order["customer_name"] == selected_customer:
                selected_order = order
                break
        updated_name = st.text_input(
            "Customer Name",
            value=selected_order["customer_name"],
            key="edit_name"
        )
        updated_coffee = st.selectbox(
            "Coffee Type",
            ["Latte", "Espresso", "Cappuccino", "Americano"],
            index=["Latte", "Espresso", "Cappuccino", "Americano"].index(selected_order["coffee_type"]),
            key="edit_coffee"
        )
        updated_size = st.selectbox(
            "Size",
            ["Small", "Medium", "Large"],
            index=["Small", "Medium", "Large"].index(selected_order["size"]),
            key="edit_size"
        )
        btn_update = st.button("Update Order", key="update_order_btn")  # Added unique key
if btn_update:
    if not updated_name:
        st.warning("Customer name cannot be empty!")
    else:
        # Update the order in session state
        selected_order["customer_name"] = updated_name
        selected_order["coffee_type"] = updated_coffee
        selected_order["size"] = updated_size

        # Save to JSON
        with open(json_path, "w") as f:
            json.dump(st.session_state["orders"], f)

        st.success("Order updated successfully!")
        st.experimental_rerun()


# Step 4: I want to show input fields pre-filled with current order values
        if selected_order:
            new_customer_name = st.text_input(
                "Customer Name",
                value=selected_order["customer_name"]
            )
            new_coffee_type = st.selectbox(
    "Coffee Type",
    ["Latte", "Espresso", "Cappuccino", "Americano"],
    key="update_coffee"
)

            new_size = st.radio(
                "Size",
                ["Small", "Medium", "Large"],
                index=["Small", "Medium", "Large"].index(selected_order["size"]),
                horizontal=True
            )

            # Step 5: Update button to save changes
            if st.button("Update Order"):
                # Update the selected order values
                selected_order["customer_name"] = new_customer_name
                selected_order["coffee_type"] = new_coffee_type
                selected_order["size"] = new_size

                # Saving updated orders to JSON
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(st.session_state["orders"], f)

                st.success("Order updated successfully!")
                st.rerun()

with tab4:
    st.header("Cancel an Order")

    # Create a list of customer names for existing orders
    order_customers = [order["customer_name"] for order in st.session_state["orders"]]

    if not order_customers:
        # If no orders exist, show a warning
        st.warning("No orders available to cancel!")
    else:
        # Letting the user select which order to cancel
        selected_customer = st.selectbox("Select Customer to Cancel", order_customers, key="cancel_customer")

        if st.button("Cancel Order"):
            # Finding the index of the selected order and remove it from the list
            for i, order in enumerate(st.session_state["orders"]):
                if order["customer_name"] == selected_customer:
                    del st.session_state["orders"][i]
                    break

            # Save updated orders to JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(st.session_state["orders"], f)

            st.success("Order cancelled successfully!")
            st.rerun()

