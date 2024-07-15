<template>
  <br><br>
  <div class="mt-150 mb-150">
    <div class="container">
      <div class="row">
        <div class="col-lg-8">
          <div class="single-article-section" v-if="post">
            <div class="single-article-text">
              <div v-if="post.image">
                <img :src="getImageUrl(post.image)" alt="Post Image" class="post-image"/>
              </div>
              <p class="blog-meta">
                <br>
                <span class="author"><span class="material-symbols-outlined" style="position:relative; top:4px;">person</span> Author - {{ fetchUserByEmail(post.user_email).user_name }} &emsp;</span>
                <span class="date"><span class="material-symbols-outlined" style="position:relative; top:4px;">calendar_month</span> {{ formatDate(post.created_at) }} </span>
              </p>
              <div class="post-options" v-if="post.user_email === currentUser">
                <a @click="togglePostOptions"><strong> . . . </strong></a>
                <div v-if="showPostOptions" class="options-menu">
                  <button @click="deletePost">Delete</button>
                </div>
              </div>
              <h2>{{ post.post_title }}</h2>
              <p>{{ post.post_desc }}</p>
            </div>

            <div class="comments-list-wrap">
              <h3 class="comment-count-title">{{ comments.length }} Comments</h3>
              <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="single-comment-body">
                  <div class="comment-user-avater">
                    <img src="../assets/img/user-image.svg" alt="User Avatar" style="width: 50px;">
                  </div>
                  <div class="comment-text-body">
                    <h4>{{ fetchUserByEmail(comment.user_email).user_name }} &emsp;<span class="comment-date">{{ formatDate(post.created_at) }}</span></h4>
                    <p>{{ comment.comments_data }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="comment-template">
              <h4>Leave a comment</h4>
              <p>If you have a comment don't hesitate to send us your opinion.</p>
              <form @submit.prevent="handleSubmit">
                <p><textarea v-model="newComment.comments_data" class="form-control" id="floatingTextarea2" rows="10" placeholder="Your Message" required></textarea></p>
                <p><input type="submit" value="Submit"></p>
              </form>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="sidebar-section">
            <div class="recent-posts">
              <h4>Recent Posts</h4>
              <ul>
                <!-- Loop and display the first 5 recent posts -->
                <li v-for="recentPost in recentPosts.slice(0, 5)" :key="recentPost.id"><a :href="`/postpage/${recentPost.id}`">{{ recentPost.post_title }}</a></li>
              </ul>
            </div>
            <div class="tag-section">
              <h4>Tags</h4>
              <ul>
                <!-- Add tags manually -->
                <li><a href="/tag/gender-violence">Gender Violence</a></li>
                <li><a href="/tag/sexual-awareness">Sexual Awareness</a></li>
                <li><a href="/tag/wellness">Wellness</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../api';

export default {
  setup() {
    const userName = ref('');
    const currentUser = ref('');

    const fetchUserDetails = async () => {
      try {
        const response = await api.getUserDetails();
        userName.value = response.data.user_name;
        currentUser.value = response.data.user_email;
      } catch (error) {
        console.error("Failed to fetch user details:", error);
      }
    };

    onMounted(() => {
      fetchUserDetails();
    });

    return {
      userName,
      currentUser
    };
  },
  data() {
    return {
      post: null,
      comments: [],
      newComment: {
        user_email: '',
        comments_data: '',
      },
      users: [],
      showPostOptions: false,
      showCommentOptions: {},
      recentPosts: []
    };
  },
  async created() {
    const postId = this.$route.params.id;
    await this.fetchPost(postId);
    await this.fetchComments(postId);
    await this.fetchUsers();
    await this.fetchRecentPosts();
  },
  watch: {
    currentUser(newEmail) {
      this.newComment.user_email = newEmail;
    }
  },
  methods: {
    async fetchPost(postId) {
      try {
        const response = await api.getPostById(postId);
        this.post = response.data;
      } catch (error) {
        console.error('Error fetching post:', error);
      }
    },
    async fetchComments(postId) {
      try {
        const response = await api.getComments(postId);
        this.comments = response.data;
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    },
    async fetchUsers() {
      try {
        const response = await api.getUsers();
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async fetchRecentPosts() {
      try {
        const response = await api.getPosts();
        this.recentPosts = response.data;
      } catch (error) {
        console.error('Error fetching recent posts:', error);
      }
    },
    fetchUserByEmail(userEmail) {
      return this.users.find(user => user.user_email === userEmail) || {};
    },
    getImageUrl(imagePath) {
      const baseUrl = 'http://localhost:8000';
      return `${baseUrl}/static/Pictures/${imagePath}`;
    },
    handleSubmit() {
      console.log('Form submitted with:', this.newComment);
      this.addComment();
    },
    async addComment() {
      try {
        const postId = this.post.id;
        const commentData = {
          post_id: postId,
          ...this.newComment,
        };
        console.log('Submitting new comment:', commentData);
        const response = await api.createComment(commentData);
        console.log('Comment creation response:', response);
        await this.fetchComments(postId);
        this.newComment = { user_email: this.currentUser, comments_data: '' };
      } catch (error) {
        console.error('Error adding comment:', error);
      }
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    togglePostOptions() {
      this.showPostOptions = !this.showPostOptions;
    },
    async deletePost() {
      try {
        await api.deletePost(this.post.id);
        this.$router.push({ name: 'posts' });
      } catch (error) {
        console.error('Error deleting post:', error);
      }
    },
    toggleCommentOptions(commentId) {
      this.$set(this.showCommentOptions, commentId, !this.showCommentOptions[commentId]);
    },
    async deleteComment(commentId) {
      try {
        await api.deleteComment(commentId);
        this.comments = this.comments.filter(comment => comment.id !== commentId);
      } catch (error) {
        console.error('Error deleting comment:', error);
      }
    }
  }
};
</script>

<style scoped>
.post-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
}

.post-title, .post-author, .post-date {
  margin: 10px 0;
}

.comment-date {
  color: gray;
}

.post-content {
  margin: 20px 0;
}

.comments-section, .add-comment-section {
  margin: 20px 0;
}

.comment {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
  position: relative;
}

.comment-author, .comment-date, .comment-content {
  margin: 5px 0;
}

.add-comment-section form {
  display: flex;
  flex-direction: column;
}

.add-comment-section input, .add-comment-section textarea {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.add-comment-section button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.post-options, .comment-options {
  position: relative;
  float: right;
  cursor: pointer;
}

.options-menu {
  position: absolute;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.options-menu button {
  display: block;
  width: 100%;
  padding: 10px;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  color: red;
}

.options-menu button:hover {
  background-color: #f5f5f5;
}
</style>
