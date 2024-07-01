<template>
  <div class="post-container" v-if="post">
    <div class="post-header">
      <div v-if="post.image">
        <img :src="post.image" alt="Post Image" class="post-image"/>
      </div>
      <div v-else>
        <h1 class="post-title">{{ post.post_title }}</h1>
        <p class="post-author">{{ getUser(post.user_id).user_name }}</p>
        <p class="post-date">Posted Date</p>
      </div>
      <div class="post-options">
        <button @click="togglePostOptions">...</button>
        <div v-if="showPostOptions" class="options-menu">
          <button @click="deletePost">Delete</button>
        </div>
      </div>
    </div>
    <div class="post-content">
      <p>{{ post.post_desc }}</p>
    </div>
    <div class="comments-section">
      <h2>Comments</h2>
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <p class="comment-author">{{ getUser(comment.user_id).user_name }}</p>
        <p class="comment-date">Posted Date</p>
        <p class="comment-content">{{ comment.comments_data }}</p>
        <div class="comment-options">
          <button @click="toggleCommentOptions(comment.id)">...</button>
          <div v-if="showCommentOptions[comment.id]" class="options-menu">
            <button @click="deleteComment(comment.id)">Delete Comment</button>
          </div>
        </div>
      </div>
    </div>
    <div class="add-comment-section">
      <h2>Leave a Comment</h2>
      <form @submit.prevent="addComment">
        <input v-model="newComment.user_name" type="text" placeholder="Your Name" required/>
        <input v-model="newComment.user_email" type="email" placeholder="Your Email" required/>
        <textarea v-model="newComment.comments_data" placeholder="Your Comment" required></textarea>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      post: null,
      comments: [],
      newComment: {
        user_name: '',
        user_email: '',
        comments_data: '',
      },
      users: [],
      showPostOptions: false,
      showCommentOptions: {}
    };
  },
  async created() {
    const postId = this.$route.params.id;
    await this.fetchPost(postId);
    await this.fetchComments(postId);
    await this.fetchUsers();
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
    getUser(userId) {
      return this.users.find(user => user.id === userId) || {};
    },
    async addComment() {
      try {
        const postId = this.post.id;
        const commentData = {
          post_id: postId,
          ...this.newComment,
        };
        await api.createComment(commentData);
        await this.fetchComments(postId); // Refresh comments after adding
        this.newComment = { user_name: '', user_email: '', comments_data: '' };
      } catch (error) {
        console.error('Error adding comment:', error);
      }
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
