<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%@page import="java.sql.DriverManager"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Statement"%>
<%@page import="java.sql.Connection"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Patient Profile</title>
<%
	String id = request.getParameter("id");
	String driverName = "com.mysql.jdbc.Driver";
	String connectionUrl = "jdbc:mysql://localhost:3306/";
	String dbName = "hospital";
	String userId = "root";
	String password = "";
%>
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
		<div class="bg-light border-right" id="sidebar-wrapper">
			<div class="sidebar-heading">Sweet Hospital</div>
			<div class="list-group list-group-flush">
				<a href="#" class="list-group-item list-group-item-action bg-light">Profile</a>
				<a href="predictor.jsp"
					class="list-group-item list-group-item-action bg-light">Predictor</a>
				<%
					String role = (String) session.getAttribute("role");
					if (role.equals("admin")) {
				%>
				<a href="patient.jsp"
					class="list-group-item list-group-item-action bg-light">Patient
					List</a>
				<%
					}
				%>
				<a href="#" class="list-group-item list-group-item-action bg-light">Settings</a>
				<a href="logout.jsp"
					class="list-group-item list-group-item-action bg-light">Logout</a>
			</div>
		</div>
		<!-- /#sidebar-wrapper -->

		<!-- Page Content -->
		<div id="page-content-wrapper">

			<nav
				class="navbar navbar-expand-lg navbar-light bg-light border-bottom">

				<div class="collapse navbar-collapse" id="navbarSupportedContent">
					<ul class="navbar-nav ml-auto mt-2 mt-lg-0">
						<li class="nav-item active"><a class="nav-link" href="#">Hello,
						</a></li>
						<li class="nav-item"><a class="nav-link" href="#"> <%
 	out.print(name);
 %>
						</a></li>
						<li class="nav-item dropdown">
							<div class="dropdown-menu dropdown-menu-right"
								aria-labelledby="navbarDropdown">
								<a class="dropdown-item" href="#">Action</a> <a
									class="dropdown-item" href="#">Another action</a>
								<div class="dropdown-divider"></div>
								<a class="dropdown-item" href="#">Something else here</a>
							</div>
						</li>
					</ul>
				</div>
			</nav>

			<div class="container-fluid">
				<%
					try {
						Class.forName(driverName);
					} catch (ClassNotFoundException e) {
						e.printStackTrace();
					}

					Connection connection = null;
					Statement statement = null;
					ResultSet resultSet = null;
					int i = 1;

					try {
						connection = DriverManager.getConnection(connectionUrl + dbName, userId, password);
						statement = connection.createStatement();
						String sql = "SELECT * FROM patient WHERE patient_id = '" + id + "'";

						resultSet = statement.executeQuery(sql);
						while (resultSet.next()) {
				%>
				<h3 class="mt-4">
					Health Data for patient:
					<%= resultSet.getString("patient_firstname")%></h1>
				<%
					}
					} catch (Exception e) {
						e.printStackTrace();
					}
				%>
				<form method="POST" action="AddData">
					<div class="form-group">
						<input type="text" class="form-control" id="bmi" name="bmi"
							placeholder="BMI" required>
					</div>

					<div class="form-group">
						<input type="text" class="form-control" name="glucose"
							id="glucose" placeholder="Glucose" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="bp" name="bp"
							placeholder="Blood Pressure" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pregnancies"
							name="pregnancies" placeholder="Pregnancies" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pedigree"
							name="pedigree" placeholder="Pedigree Function" required>
					</div>

					<button class="btn btn-primary">Submit</button>
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