<template>
	<div class="container">
		<div class="row">
			<div class="col-md-3">
				<div class="leftbar">
					<div class="user-details">
						<img src="../assets/img/user-image.svg" class="img-fluid rounded-circle" alt="Profile Image">
						<h4>{{ firstName }} {{ lastName }}</h4>
						<p>{{ userEmail }}</p>
					</div>
					<div class="common-features">
						<ul>
							<li><a href="#">My Posts</a></li>
							<li><a href="#">Notifications</a></li>
							<li><a href="#">My Messages</a></li>
							<li><a href="#">Settings</a></li>
						</ul>
					</div>
				</div>
			</div>
			<div class="col-md-9">
				<div class="main-section">
					<h2>User Account</h2>
					<div class="change-password">
						<h3>Change Password</h3>
						<form @submit.prevent="changePassword">
							<div class="form-group">
								<input type="password" v-model="currentPassword" placeholder="Current Password" id="current-password" class="form-control">
							</div>
							<div class="form-group">
								<input type="password" v-model="newPassword" placeholder="New Password" id="new-password" class="form-control">
							</div>
							<div class="form-group">
								<input type="password" v-model="confirmNewPassword" placeholder="Confirm New Password" id="confirm-new-password" class="form-control">
							</div>
							<button id="change-password-btn" class="btn btn-primary">Change Password</button>
						</form>
					</div>
					<div class="customize-image">
						<h3>Customize Profile Image</h3>
						<input type="file" id="profile-image-upload" class="form-control-file">
						<button id="upload-image-btn" class="btn btn-primary">Upload Image</button>
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
		const userEmail = ref('');
		const firstName = ref('');
		const lastName = ref('');
		const userImage = ref('');
		const currentPassword = ref('');
		const newPassword = ref('');
		const confirmNewPassword = ref('');

		const fetchUserDetails = async () => {
			try {
				const response = await api.getUserDetails();
				userEmail.value = response.data.user_email;
				firstName.value = response.data.first_name;
				lastName.value = response.data.last_name;
				userImage.value = response.data.user_image;
			} catch (error) {
				console.error("Failed to fetch user details:", error);
			}
		};

		const updatePassword = async (email, currentPassword, newPassword) => {
			try {
				const passwordData = {
					old_password: currentPassword,
					new_password: newPassword
				};
				await api.updatePassword(email, passwordData);
				alert('Password updated successfully');
			} catch (error) {
				console.error("Failed to update password:", error);
				alert('Failed to update password');
			}
		};

		const changePassword = () => {
			if (newPassword.value !== confirmNewPassword.value) {
				alert('New password and confirm password do not match');
				return;
			}

			updatePassword(userEmail.value, currentPassword.value, newPassword.value);
		};

		/**const handleImageUpload = (event) => {
			const file = event.target.files[0];
		};

		const uploadImage = async () => {
			// this is not implemented in the API yet
		};**/

		onMounted(() => {
			fetchUserDetails();
		});

		return {
			userEmail,
			firstName,
			lastName,
			userImage,
			currentPassword,
			newPassword,
			confirmNewPassword,
			changePassword
			/**
			 * handleImageUpload,
			 * uploadImage
			*/
		};
	},
}
</script>

<style>
.leftbar {
	padding: 20px;
	background-color: #f5f5f5;
}

.user-details {
	text-align: center;
}

.user-details img {
	width: 150px;
	height: 150px;
	object-fit: cover;
	margin-bottom: 10px;
}

.main-section {
	padding: 20px;
}

.change-password,
.customize-image {
	margin-top: 20px;
}
</style>