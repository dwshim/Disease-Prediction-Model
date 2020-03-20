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
		<%@ include file = "template.jsp" %>
		<!-- /#sidebar-wrapper -->

		<!-- Page Content -->
		<div id="page-content-wrapper">

			<div class="container-fluid">
				<h1 class="mt-4">Add Patient</h1>
				
				<form method="POST" action="addpatient">
					<div class="form-group">
						<input type="text" class="form-control" id="first" name="first" placeholder="First Name"
							required>
					</div>

					<div class="form-group">
						<input type="text" class="form-control" name="last" id="last"
							placeholder="Last Name" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="department" name="department"
							placeholder="Department" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="address" name="address"
							placeholder="Address" required>
					</div>
					<div class="form-group">
						<textarea class="form-control" id="prescription" rows = "5" name="prescription"
							placeholder="Prescription" required></textarea>
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