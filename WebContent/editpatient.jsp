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
				<h1 class="mt-4">Edit Patient Data</h1>

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
						String sql = "SELECT * FROM `patient` WHERE `patient_id` = '" + request.getParameter("id") + "'";

						resultSet = statement.executeQuery(sql);
						while (resultSet.next()) {
				%>
				<form method="POST" action="updatepatient">
					<div class="form-group">
					<label for="bmiinput">First Name</label>
						<input type="text" class="form-control" id="firstname" name="firstname"
							placeholder="First Name" value="<%=resultSet.getString("patient_firstname")%>"
							required>
					</div>

					<div class="form-group">
					<label for="glucoseinput">Last Name</label>
						<input type="text" class="form-control" name="lastname"
							id="lastname" placeholder="Last Name"
							value="<%=resultSet.getString("patient_lastname")%>" required>
					</div>
					<div class="form-group">
					<label for="bpinput">Address</label>
						<input type="text" class="form-control" id="address" name="address"
							placeholder="Address"
							value="<%=resultSet.getString("address")%>" required>
					</div>
					<div class="form-group">
					<label for="pregnanciesinput">Department</label>
						<input type="text" class="form-control" id="department"
							name="department" placeholder="Department"
							value="<%=resultSet.getString("department")%>" required>
					</div>
					<div class="form-group">
					<label for="pedigreeinput">Prescription</label>
						<input type="text" class="form-control" id="prescription"
							name="prescription" placeholder="Prescription"
							value="<%=resultSet.getString("prescription")%>" required>
					</div>
					<div class="form-group">
						<input type="hidden" class="form-control" id="patientid"
							name="patientid" value="<%=resultSet.getString("patient_id")%>">
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