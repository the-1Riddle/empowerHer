<template>
	<br>
	<div class="container">
	  <div class="row">
	    <div class="col-md-6 offset-md-3">
	      <div class="card">
	        <div class="card-header">
	          <h2>User Account</h2>
	        </div>
	        <div class="card-body">
	          <div class="user-details">
	            <p><strong>Username:</strong> <span id="username"></span></p>
	            <p><strong>Email:</strong> <span id="useremail"></span></p>
	            <p><strong>Profile Image:</strong> <img src="" id="profile-image" class="img-fluid rounded-circle" alt="Profile Image"></p>
	          </div>
	          <div class="change-password">
	            <h3>Change Password</h3>
	            <form>
	              <div class="form-group">
	                <input type="password" placeholder="Current Password" id="current-password" class="form-control">
	              </div>
	              <div class="form-group">
	                <input type="password" placeholder="New Password" id="new-password" class="form-control">
	              </div>
	              <div class="form-group">
	                <input type="password" placeholder="Confirm New Password" id="confirm-new-password" class="form-control">
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
	</div>
</template>

<script>
	
</script>