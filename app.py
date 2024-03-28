import streamlit as st

# st.markdown(
#     """
#     <style>
#     .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
#     .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
#     .viewerBadge_text__1JaDK {
#         display: none;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)


st.write("!2312")