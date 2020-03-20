<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Add Patient</title>

<!-- Bootstrap core CSS -->
<link href="css/bootstrap.min.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="css/simple-sidebar.css" rel="stylesheet">

</head>
<body>
	<%
		String name = (String) session.getAttribute("username");
		if (name == null) {
			response.sendRedirect("login.jsp");
		}
	%>
	<div class="d-flex" id="wrapper">

		<!-- Sidebar -->
		<%@ include file="template.jsp"%>
		<!-- /#sidebar-wrapper -->

		<!-- Page Content -->
		<div id="page-content-wrapper">

			<div class="container-fluid">
				<h1 class="mt-4">Add new employee</h1>

				<form method="POST" action="addemployee">
					<div class="form-group">
						<input type="text" class="form-control" id="user" name="username"
							placeholder="Username" required>
					</div>

					<div class="form-group">
						<input type="password" class="form-control" name="password"
							id="pass" placeholder="Password" required>
					</div>
					<div class="form-group">
						<select class ="browser-default custom-select" id="role" name="role">
							<option value="Hospital Specialist">Hospital Specialist</option>
							<option value="Patient Administrator">Patient Administrator</option>
							<option value="System Administrator">System Administrator</option>
							<option value="Lab Specialist">Lab Specialist</option>
						</select>
					</div>
					<div class="form-group">
						<select class ="browser-default custom-select" id="title" name="title">
							<option value="Doctor">Doctor</option>
							<option value="Nurse">Nurse</option>
							<option value="Lab Assistant">Lab Assistant</option>
							<option value="Radiologist">Radiologist</option>
							<option value="IT Admin">IT Admin</option>
							<option value="Data Scientist">Data Scientist</option>
						</select>
					</div>

					<button class="btn btn-primary">Add</button>
				</form>
			</div>
		</div>
		<!-- /#page-content-wrapper -->

	</div>
	<!-- /#wrapper -->

	<!-- Bootstrap core JavaScript -->
	<script src="vendor/jquery/jquery.min.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

	<!-- Menu Toggle Script -->
	<script>
		$("#menu-toggle").click(function(e) {
			e.preventDefault();
			$("#wrapper").toggleClass("toggled");
		});
	</script>
</body>
</html>