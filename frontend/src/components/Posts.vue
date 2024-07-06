<template>
  <div class="post-list">
    <div v-for="post in paginatedPosts" :key="post.id" class="post-card">
      <img v-if="post.image" :src="getImageUrl(post.image)" alt="Post image" class="post-image"/>
      <div v-else class="post-placeholder">{{ getPlaceholderText(post.post_desc, 10) }}</div>
      <div class="post-content">
        <h3>{{ post.post_title }}</h3>
        <div class="post-meta">
          <span class="author"><i class="fa fa-user"></i> Author - </span>
          <span class="date"><i class="fa fa-calendar"></i> {{ formatDate(post.date) }}</span>
        </div>
        <p>{{ post.post_desc }}</p>
        <router-link :to="{ name: 'postpage', params: { id: post.id } }" class="read-more">read more</router-link>
      </div>
    </div>
  </div>
  <nav aria-label="Page navigation example">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{ disabled: currentPage === 1 }" @click="prevPage">
        <a class="page-link">Previous</a>
      </li>
      <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: page === currentPage }" @click="goToPage(page)">
        <a class="page-link">{{ page }}</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === totalPages }" @click="nextPage">
        <a class="page-link">Next</a>
      </li>
    </ul>
  </nav>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      posts: [],
      currentPage: 1,
      postsPerPage: 12,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.posts.length / this.postsPerPage);
    },
    paginatedPosts() {
      const start = (this.currentPage - 1) * this.postsPerPage;
      const end = start + this.postsPerPage;
      return this.posts.slice(start, end);
    },
  },
  async created() {
    await this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await api.getPosts();
        this.posts = response.data;
      } catch (error) {
        console.error('Error fetching posts:', error);
        alert('Error fetching posts. Please try again later.');
      }
    },
    getImageUrl(imagePath) {
      return `http://localhost:8000/static/Pictures/${imagePath}`;
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    getPostDescription(post) {
      if (post.image) {
        return this.getPlaceholderText(post.description, 15);
      } else {
        return this.getPlaceholderText(post.description, 50);
      }
    },
    getPlaceholderText(text, numWords) {
      const words = text.split(' ');
      return words.slice(0, numWords).join(' ');
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
  },
};
</script>

<style scoped>
.post-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.post-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
  width: 300px;
}
.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.post-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  background-color: #f5f5f5;
  color: #aaa;
  text-align: center;
  padding: 20px;
}
.post-content {
  padding: 20px;
  color: black;
}
.post-content h3 {
  margin: 0 0 10px;
  color: lightseagreen;
}
.post-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
.post-meta .author,
.post-meta .date {
  color: #aaa;
  font-size: 0.9em;
}
.post-content p {
  margin: 0 0 10px;
}
.read-more {
  color: #007bff;
  text-decoration: none;
}
.read-more:hover {
  text-decoration: underline;
}
.pagination {
  display: flex;
  align-items: center;
  margin-top: 20px;
}
.pagination li {
  cursor: pointer;
}
.pagination li:disabled {
  cursor: not-allowed;
}
.pagination span {
  margin: 0 5px;
}
</style>