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
<title>Editor</title>
<%
	String id = request.getParameter("id");
	String driverName = "com.mysql.jdbc.Driver";
	String connectionUrl = "jdbc:mysql://localhost:3306/";
	String dbName = "hospital";
	String userId = "root";
	String password = "";
%>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
				<h1 class="mt-4">Edit User Information</h1>

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
						String sql = "SELECT * FROM `user` WHERE `employee_id` = '" + request.getParameter("id") + "'";

						resultSet = statement.executeQuery(sql);
						while (resultSet.next()) {
				%>
				<form method="POST" action="updateuser">
					<div class="form-group">
						<label for="bmiinput">Username</label> <input type="text"
							class="form-control" id="username" name="username"
							placeholder="Username"
							value="<%=resultSet.getString("username")%>" required>
					</div>

					<div class="form-group">
						<label for="glucoseinput">Password</label> <input type="password"
							class="form-control" name="password" id="password"
							placeholder="Password"
							value="<%=resultSet.getString("password")%>" required>
					</div>
					<div class="form-group">
						<label for="pedigreeinput">Role</label>
						<br>
						<select
							class="browser-default custom-select" id="role" name="role">
							<option value="Hospital Specialist">Hospital Specialist</option>
							<option value="Patient Administrator">Patient
								Administrator</option>
							<option value="System Administrator">System
								Administrator</option>
							<option value="Lab Specialist">Lab Specialist</option>
						</select>
					</div>
					<div class="form-group">
					<label for="pedigreeinput">Title</label>
					<br>
						<select class ="browser-default custom-select" id="title" name="title">
							<option value="Doctor">Doctor</option>
							<option value="Nurse">Nurse</option>
							<option value="Lab Assistant">Lab Assistant</option>
							<option value="Radiologist">Radiologist</option>
							<option value="IT Admin">IT Admin</option>
							<option value="Data Scientist">Data Scientist</option>
						</select>
					</div>
					<div class="form-group">
						<input type="hidden" class="form-control" id="employeeid"
							name="employeeid" value="<%=resultSet.getString("employee_id")%>">
					</div>

					<button class="btn btn-primary">Submit</button>
				</form>

				<%
					}

					} catch (Exception e) {
						e.printStackTrace();
					}

					connection.close();
				%>
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