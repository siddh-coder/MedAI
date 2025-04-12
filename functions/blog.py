import streamlit as st
from utils.database import get_blog_posts, add_blog_post, get_user_by_id

def show():
    st.title("Health Blogs")
    st.markdown("Explore our collection of health and wellness articles.")
    
    categories = ["All", "Transforming Healthcare", "Holistic Health", "Nourishing Body", "Importance of Games"]
    selected_category = st.selectbox("Filter by Category", categories)
    
    category = None if selected_category == "All" else selected_category
    blogs = get_blog_posts(category=category, limit=10)
    
    if st.session_state.user_type in ['doctor', 'admin']:
        st.subheader("Create New Blog Post")
        with st.form("blog_form"):
            title = st.text_input("Title")
            content = st.text_area("Content", height=200)
            blog_category = st.selectbox("Category", categories[1:])
            submit = st.form_submit_button("Publish")
            
            if submit:
                if not title or not content:
                    st.error("Please fill in all fields.")
                else:
                    blog_id = add_blog_post(
                        title=title,
                        content=content,
                        author_id=st.session_state.user['id'],
                        category=blog_category
                    )
                    st.success("Blog post published!")
                    st.rerun()
    
    st.subheader("Recent Posts")
    if not blogs:
        st.info("No blog posts available in this category.")
    else:
        for blog in blogs:
            with st.expander(blog['title']):
                st.write(f"**Author**: {blog['author_name']}")
                st.write(f"**Category**: {blog['category']}")
                st.write(f"**Published**: {blog['created_at'].strftime('%Y-%m-%d')}")
                st.write(f"**Views**: {blog['views']}")
                st.markdown(blog['content'])
