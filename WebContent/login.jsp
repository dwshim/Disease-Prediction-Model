<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html lang="en">
<head>
<title>Cancer Predictor Login</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
<link rel="stylesheet" type="text/css" href="css/util.css">
<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>
	<script language="javascript">
		$(function() {
			// set a event handler to the button
			$("#login100-form-btn").click(function() {
				// retrieve form data
				var uname = $("#uname").val();
				var pass = $("#pass").val();

				// send form data to the server side php script.
				$.ajax({
					type : "POST",
					url : "checkPassword.php",
					data : {
						uname : uname,
						pass : pass
					}
				}).done(function(data) {

					// Now the output from PHP is set to 'data'.
					// Check if the 'data' contains 'OK' or 'NG'
					if (data.indexOf("OK") >= 0) {

						// you can do something here
						alert("Login Successed.");
						location.href = "home.jsp";

					} else if (data.indexOf("NG") >= 0) {

						// you can do something here
						alert("Login Failed.");
						location.href = "error.jsp";
					}
				});
			});
		});
	</script>
	<div class="limiter">
		<div class="container-login100">
			<div class="wrap-login100 p-b-160 p-t-50">
				<form class="login100-form validate-form" method="post"
					action="Login">
					<span class="login100-form-title p-b-43"> Account Login </span>

					<div class="wrap-input100 rs1 validate-input"
						data-validate="Username is required">
						<input class="input100" type="text" name="username" id="uname"> <span
							class="label-input100">Username</span>
					</div>

					<div class="wrap-input100 rs2 validate-input"
						data-validate="Password is required">
						<input class="input100" type="password" name="pass" id="pass"> <span
							class="label-input100">Password</span>
					</div>

					<div class="container-login100-form-btn">
						<button class="login100-form-btn">Sign in</button>
					</div>

				</form>
			</div>
		</div>
	</div>





	<!--===============================================================================================-->
	<script src="js/jquery-3.2.1.min.js"></script>
	<script src="js/main.js"></script>

</body>
</html>