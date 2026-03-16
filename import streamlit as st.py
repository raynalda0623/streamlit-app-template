import streamlit as st
import time
import json
from pathlib import Path


st.set_page_config(
    page_title="Course Manager",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)




st.title("Course Management App")

st.divider()

next_assignment_id_number = 3

#load assignments
assignments = [
    {
        "id" : "HW1",
        "title" : "Introduction to Database",
        "description": "basics of database design",
        "points" : 100,
        "type" : "homework"
    },
    {
        "id": "HW2",
        "title": "Normalization",
        "description" : "Normalize the table designs",
        "points": 100,
        "type" : "lab"
    }
]

json_path = Path("assignments.json")

if json_path.exists():
    with json_path.open("r", encoding= "utf-8") as f:
        assignments = json.load(f)




tab1, tab2, tab3 = st.tabs(["View Assignments", "Add New Assignment", "Update An Assignment"])

with tab1:
    #st.info("This tab is under development!")
    option = st.radio("View/Search", ["View" , "Search"], horizontal= True)

    if option == "View":
        st.dataframe(assignments)

    else:
        titles = []
        for assignmnet in assignments:
            titles.append(assignmnet["title"])

        if not titles:
            st.warning("No Assignmnet is found")
        else:
            selected_title = st.selectbox("Assignmnet Title", titles)

            for assignment in assignments:
                if assignment["title"] == selected_title:
                    with st.expander( 'Assignment Details', expanded=True):
                        st.markdown(f"### Ttitle: {assignment['title']}")
                        st.markdown(f"Description: {assignment['description']}")
                        st.markdown(f"Type: **{assignment['type']}**")
                    break
            
            selected_assignment = st.selectbox('Assignment Title',
                                          options=assignments,
                                          format_func=lambda x: f"{x['title']}",
                                          key= 'new_assignment')
            
            with st.expander( 'Assignment Details', expanded=True):
                st.markdown(f"### Ttitle: {selected_assignment['title']}")
                st.markdown(f"Description: {selected_assignment['description']}")
                st.markdown(f"Type: **{selected_assignment['type']}**")
        
with tab2:
    # Add New Assignment
    st.markdown("# Add New Assignment")

    #input

    title = st.text_input("Title",placeholder="ex. Homework 1", 
                        help="This is the name of the assignment")

    description = st.text_area("Description",placeholder="ex. database design...")
    due_date = st.date_input("Due Date")
    assignments_type = st.radio("Type",["Homework", "Lab"])

    points = st.number_input("Points")

    #assignments_type2 = st.selectbox("Type", ["Homework", "Lab","Other"])
    #if assignments_type2 == "Other":
    #   assignments_type2 = st.text_input("Assingment Type")

    #lab = st.checkbox("Lab")

    with st.expander("Assignment Preview",expanded= True):
        st.markdown("## Live Preview")
        st.markdown(f"Title: {title}")

    btn_save = st.button("Save",use_container_width=True, disabled=False,type="")


   

    if btn_save:
        with st.spinner("Saving the Assignmnet..."):
            time.sleep(5)
            if not title:
                st.warning("Enter Assignmnet Title")
            else:
                #Add/Create new Assignmnet
                new_assignmnet_id = "HW" + str(next_assignment_id_number)
                next_assignment_id_number += 1

                assignments.append(
                    {
                    "id" : new_assignmnet_id,
                    "title": title,
                    "description" : description,
                        "points" : points,
                        "type" : assignments_type
                    }
                )

                with json_path.open("w",encoding="utf-8") as f:
                    json.dump(assignments,f)

                time.sleep(4)
                st.success("Assignment is recorded!")
                st.rerun()
                st.dataframe(assignments)

with tab3:
    st.markdown("# Update an Assignment")

    titles = []
    for assignment in assignments:
        titles.append(assignment["title"])

    selected_item = st.selectbox("Select an item", titles,key="search_titles")
    
    selected_assignment = {}
    for assignment in assignments:
        if assignment["title"] == selected_item:
            selected_assignment = assignment
            break

    edit_title = st.text_input("Title", value = selected_assignment['title'], 
                               key=f"edit_title_{selected_assignment['id']}")
    edit_description = st.text_area("Description", value= selected_assignment['description'], 
                                    key = f"edit_description_{selected_assignment['id']}")
    
    type_list = ["Homework", "Lab"]
    selected_assignmnet_type_index = type_list.index(selected_assignment['type'].capitalize())

    edit_type = st.radio("Type", type_list, index=selected_assignmnet_type_index,
                         key= f"edit_type_{selected_assignment['id']}" )


    update_btn = st.button("Update Assignment",key="btn_update",use_container_width=True,type="primary")
    if update_btn:
        with st.spinner("Updating the assignment..."):
            time.sleep(5)
            selected_assignment['title'] = edit_title
            selected_assignment["description"] = edit_description

            with json_path.open("w",encoding="utf-8") as f:
                json.dump(assignments,f)

            st.success("Assignment is updated!")
            time.sleep(5)
            st.rerun()


           # st.dataframe(assignments)





with st.sidebar:
    st.markdown("This is a sidebar")
    if st.button("Log out", type="primary",use_container_width=True):
        time.sleep(5)
        st.success("you are being logged out!")