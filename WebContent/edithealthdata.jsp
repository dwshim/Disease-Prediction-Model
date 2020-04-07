<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%@page import="java.sql.DriverManager"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Statement"%>
<%@page import="java.sql.Connection"%>
<%@page import="com.predictive.DatabaseInfo"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Editor</title>
<%
	String id = request.getParameter("id");
	String driverName = "com.mysql.jdbc.Driver";
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
				<h1 class="mt-4">Edit Data</h1>

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
						connection = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL  + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS);
						statement = connection.createStatement();
						String sql = "SELECT * FROM `patient_data` WHERE `patient_id` = '" + request.getParameter("id") + "'";

						resultSet = statement.executeQuery(sql);
						while (resultSet.next()) {
				%>
				<form method="POST" action="update">
					<div class="form-group">
					<label for="bmiinput">Concave Points Mean</label>
						<input type="text" class="form-control" id="bmi" name="bmi"
							placeholder="BMI" value="<%=resultSet.getString("bmi")%>"
							required>
					</div>

					<div class="form-group">
					<label for="glucoseinput">Radius Worst</label>
						<input type="text" class="form-control" name="glucose"
							id="glucose" placeholder="Glucose"
							value="<%=resultSet.getString("glucose")%>" required>
					</div>
					<div class="form-group">
					<label for="bpinput">Perimeter Worst</label>
						<input type="text" class="form-control" id="bp" name="bp"
							placeholder="Blood Pressure"
							value="<%=resultSet.getString("bloodp")%>" required>
					</div>
					<div class="form-group">
					<label for="pregnanciesinput">Area Worst</label>
						<input type="text" class="form-control" id="pregnancies"
							name="pregnancies" placeholder="Pregnancies"
							value="<%=resultSet.getString("pregnancies")%>" required>
					</div>
					<div class="form-group">
					<label for="pedigreeinput">Concave Points Worst</label>
						<input type="text" class="form-control" id="pedigree"
							name="pedigree" placeholder="Pedigree"
							value="<%=resultSet.getString("pedigree")%>" required>
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