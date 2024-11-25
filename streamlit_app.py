# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# option = st.selectbox(
#     'What is your favourite fruit? ',
#     ('Banana', 'Strawberries', 'Peaches')
# )

# st.write('You selected : ',  option)


session = get_active_session()

nameonorder_string = ''

nameonsmothie_tb = st.text_input("Name on Smoothie!")
st.write('The name on Smoothie will be : ',  nameonsmothie_tb)

nameonorder_string = nameonsmothie_tb

my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
        'Choose upto 5 ingredients : ' ,my_dataframe,max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    insert_stmt = """ insert into SMOOTHIES.public.ORDERS(ingredients,name_on_order)
                  values('""" + ingredients_string + """',' """ + nameonorder_string + """')"""
    st.write(insert_stmt) 

    submit_btn = st.button("Submit Order")

    if submit_btn:        
       if insert_stmt:
           session.sql(insert_stmt).collect()
           st.success('Your smoothie is orderd!' + nameonorder_string ,icon="❄️")

   


