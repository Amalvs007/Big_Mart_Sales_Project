import streamlit as st 
import pandas as pd 
import joblib
import pickle
from PIL import Image

st.set_page_config(layout="wide")

# Load the model file
model = joblib.load("model.pkl")
scale = joblib.load("scale.pkl")
label_Item_Type = joblib.load("label_Item_Type.pkl")

st.title(":violet[Big Mart Sales Prediction Using AI] :shopping_bags:")

image = Image.open("Shopping1.jpg")
st.image(image,use_column_width=True)


st.write('#')

st.subheader(":green[Please fill the following Fields :]")

st.write("#####")

col1,col2 = st.columns(2)

with col1:
    item_weight = st.number_input('**Item Weight**')
with col2:
    item_visibility = st.number_input('**Item Visibility**')

item_type = st.selectbox('**Item Type**',['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables',
       'Household', 'Baking Goods', 'Snack Foods', 'Frozen Foods',
       'Breakfast', 'Health and Hygiene', 'Hard Drinks', 'Canned',
       'Breads', 'Starchy Foods', 'Others', 'Seafood'])

col3,col4 = st.columns(2)

with col3:
    outlet_identifier = st.selectbox('**Outlet Identifier**',['OUT049', 'OUT018', 'OUT010', 'OUT013', 'OUT027', 'OUT045',
       'OUT017', 'OUT046', 'OUT035', 'OUT019'])
    outlet_size = st.radio('**Outlet Size**',['High','Medium','Small'])
    outlet_type = st.radio('**Outlet Type**',['Supermarket Type1', 'Supermarket Type2','Supermarket Type3','Grocery Store',])


with col4:
    outlet_establishment_year = st.selectbox('**Outlet Establishment Year**',[1999, 2009, 1998, 1987, 1985, 2002, 2007, 1997, 2004])
    outlet_location_type = st.radio('**Outlet Location Type**',['Tier 1', 'Tier 2', 'Tier 3'])
    item_fat_content = st.radio('**Item Fat Content**',["Low Fat","Regular"])

item_mrp = st.number_input('**Item MRP**')

# Converting Categorical Values to Numerical Values

item_type = pd.Series(item_type)
item_type=label_Item_Type.transform(item_type)[0]

if item_fat_content == "Regular":
    item_fat_content = 2
elif item_fat_content == "Low Fat":
    item_fat_content = 1

if outlet_size == "High":
    outlet_size = 1
elif outlet_size == "Medium":
    outlet_size = 2
elif outlet_size == "Small":
    outlet_size = 3

if outlet_type == "Supermarket Type1":
    outlet_type = 1
elif outlet_type == "Supermarket Type2":
    outlet_type = 2
elif outlet_type == "Supermarket Type3":
    outlet_type = 3
elif outlet_type == "Grocery Store":
    outlet_type = 4

outlet_location_type = int(outlet_location_type.split(" ")[1])
outlet_identifier = int(outlet_identifier.split("0")[1])

st.write("#")

col5,col6,col7,col8,col9 = st.columns(5)

with col7:
    button = st.button("Predict Sales")


if button:

    print(item_weight,item_visibility,item_type,outlet_identifier,outlet_size,outlet_type,item_mrp,item_fat_content,outlet_establishment_year,outlet_location_type)
    row_df = pd.DataFrame([pd.Series([item_weight,item_visibility,item_type,outlet_identifier,outlet_size,outlet_type,item_mrp,item_fat_content,outlet_establishment_year,outlet_location_type])])
    row_df_new = pd.DataFrame(scale.transform(row_df))

    # Model Prediction

    prediction = model.predict(row_df_new)
    st.subheader("Predicted Sales for the Above Values 	:blush::shopping_trolley:")

    st.success(f"The Predicted Sale Value is : **{round(prediction[0],2)}**")
    print(prediction[0])
    st.snow()
