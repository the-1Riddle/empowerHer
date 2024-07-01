import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  getPosts() {
    return apiClient.get('/posts/');
  },
  getPostById(postId) {
    return apiClient.get(`/posts/${postId}`);
  },
  createPost(postData) {
    return apiClient.post('/posts/', postData);
  },
  deletePost(postId) {
    return apiClient.delete(`/posts/${postId}`);
  },
  getUsers() {
    return apiClient.get('/users/');
  },
  async createUser(userData) {
    try {
      const response = await apiClient.post('/users/', userData);
      return response;
    } catch (error) {
      // Log error response for debugging
      console.error('API Error:', error.response);
      throw error;
    }
  },
  deleteUser(userId) {
    return apiClient.delete(`/users/${userId}`);
  },
  getComments(postId) {
    return apiClient.get(`/comments?post_id=${postId}`);
  },
  createComment(commentData) {
    return apiClient.post('/comments/', commentData);
  },
  deleteComment(commentId) {
    return apiClient.delete(`/comments/${commentId}`);
  },
  loginUser(loginData) {
    return apiClient.post('/login/', loginData);
  },
  signupUser(signupData) {
    return apiClient.post('/users/', signupData);
  }
};
