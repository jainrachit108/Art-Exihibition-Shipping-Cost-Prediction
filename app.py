import streamlit as st
from ShippingCost.pipeline.prediction_pipeline import ShippingData


def app():
    st.set_page_config(page_title="Shipping Cost Prediction App")
    st.title("Shipping Cost Prediction App")

    artist_reputation = st.number_input("Artist Reputation (0 to 1)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    height = st.number_input("Height (in cm)", min_value=0, max_value=None, value=100)
    width = st.number_input("Width (in cm)", min_value=0, max_value=None, value=50)
    weight = st.number_input("Weight (in kg)", min_value=0, max_value=None, value = 250)
    material = st.selectbox("Material", ["Wood", "Brass", "Aluminium", "Bronze", "Marble"])
    base_price = st.number_input("Base Price (in USD)", min_value=0, max_value=None, value=200)
    price = st.number_input("Price (in USD)", min_value=0, max_value=None, value=250)
    international = st.selectbox("International", ["Yes", "No"])
    express_shipment = st.selectbox("Express Shipment", ["Yes", "No"])
    installation_included = st.selectbox("Installation Included", ["Yes", "No"])
    transportation = st.selectbox("Transportation Included", ["Yes", "No"])
    fragile = st.selectbox("Fragile", ["Yes", "No"])
    customer_info = st.selectbox("Customer Information", ["Wealthy", "Working"])
    remote_location = st.selectbox("Remote Location", ["Yes", "No"])

    if st.button("Predict Shipping Cost"):
        data = ShippingData(artist_reputation=artist_reputation, height=height, width=width, weight=weight, material=material,
                            base_price=base_price, price=price, international=international, express_shipment=express_shipment,
                            customer_info=customer_info, fragile=fragile, installation_included=installation_included,
                            remote_location=remote_location, transportation=transportation)

        cost = data.predict()
        st.success(f"The estimated shipping cost is {cost[0]:.2f} USD")


if __name__ == '__main__':
    app()
