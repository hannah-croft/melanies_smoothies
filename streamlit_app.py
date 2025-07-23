# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)
#st.write("Your favourite fruit is:", option)


# Display the Fruit Options List
#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)


#   The Data Returned is both a list and a LIST:

#   We are placing the multiselect entries into a variable called "ingredients."
#   We can then write "ingredients" back out to the screen.
#   Our ingredients variable is an object or data type called a LIST.
#   So it's a list in the traditional sense of the word, but it is also a datatype
#   or object called a LIST. A LIST is different than a DATAFRAME which is also
#   different from a STRING!
#   We can use the st.write() and st.text() methods to take a closer look at what
#   is contained in our ingredients LIST.

# Display the LIST
#st.write(ingredients_list)
#st.text(ingredients_list)


#   Cleaning Up Empty Brackets:
#   Run your entry form (SiS App) without any ingredients in the selection box.
#   Notice the empty brackets. Those look ugly.

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""
    
    #st.write(my_insert_stmt)
    #st.stop()   # The streamlit stop command is great for troubleshooting

    time_to_insert = st.button('Submit Order')

    # Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
