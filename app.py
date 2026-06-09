import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="EduPro Instructor Analytics",
    layout="wide"
)

st.title("🎓 EduPro Instructor & Course Analytics Dashboard")

# ---------------------------
# Load Data
# ---------------------------
teachers = pd.read_csv("teacher_data.csv")
courses = pd.read_csv("Course_data1.csv")
transactions = pd.read_csv("transaction_data1.csv")

# ---------------------------
# Merge Data
# ---------------------------
merged = transactions.merge(
    teachers,
    on="TeacherID"
).merge(
    courses,
    on="CourseID"
)

# ---------------------------
# KPI Section
# ---------------------------
avg_teacher_rating = round(
    teachers["TeacherRating"].mean(), 2
)

avg_course_rating = round(
    courses["CourseRating"].mean(), 2
)

total_teachers = teachers["TeacherID"].nunique()
total_courses = courses["CourseID"].nunique()
total_enrollments = len(transactions)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Teachers", total_teachers)
col2.metric("Courses", total_courses)
col3.metric("Enrollments", total_enrollments)
col4.metric("Avg Teacher Rating", avg_teacher_rating)
col5.metric("Avg Course Rating", avg_course_rating)

st.markdown("---")

# ---------------------------
# Teacher Rating Distribution
# ---------------------------
st.subheader("Teacher Rating Distribution")

fig, ax = plt.subplots(figsize=(8,5))

teachers["TeacherRating"].hist(
    bins=10,
    ax=ax
)

ax.set_title("Distribution of Teacher Ratings")
ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Count")

st.pyplot(fig)

# ---------------------------
# Top 10 Teachers
# ---------------------------
st.subheader("Top 10 Teachers by Rating")

top_teachers = teachers.sort_values(
    by="TeacherRating",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,5))

ax.bar(
    top_teachers["TeacherName"],
    top_teachers["TeacherRating"]
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Experience vs Rating
# ---------------------------
st.subheader("Experience vs Teacher Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=teachers,
    x="YearsOfExperience",
    y="TeacherRating",
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Teacher Rating vs Course Rating
# ---------------------------
st.subheader("Teacher Rating vs Course Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=merged,
    x="TeacherRating",
    y="CourseRating",
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Course Category Analysis
# ---------------------------
st.subheader("Average Course Rating by Category")

category_rating = courses.groupby(
    "CourseCategory"
)["CourseRating"].mean().sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(10,5))

category_rating.plot(
    kind="bar",
    ax=ax
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Course Level Analysis
# ---------------------------
st.subheader("Average Course Rating by Level")

level_rating = courses.groupby(
    "CourseLevel"
)["CourseRating"].mean()

fig, ax = plt.subplots(figsize=(8,5))

level_rating.plot(
    kind="bar",
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Expertise Analysis
# ---------------------------
st.subheader("Average Teacher Rating by Expertise")

expertise_rating = teachers.groupby(
    "Expertise"
)["TeacherRating"].mean().sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(10,5))

expertise_rating.plot(
    kind="bar",
    ax=ax
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Enrollment Analysis
# ---------------------------
st.subheader("Top 10 Instructors by Enrollments")

enrollment_by_teacher = merged.groupby(
    "TeacherName"
)["TransactionID"].count().sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(10,5))

enrollment_by_teacher.head(10).plot(
    kind="bar",
    ax=ax
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ---------------------------
# Data Tables
# ---------------------------
st.markdown("---")

st.subheader("Teacher Dataset")
st.dataframe(teachers)

st.subheader("Course Dataset")
st.dataframe(courses)

st.subheader("Merged Dataset")
st.dataframe(merged.head(100))

st.success("Dashboard Loaded Successfully ✅")
