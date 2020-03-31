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
<title>Search Result</title>
<%
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
				<h1 class="mt-4">Search Result</h1>
				<table class="table">
					<thead>
						<tr>
							<th scope="col">ID</th>
							<th scope="col">First Name</th>
							<th scope="col">Last Name</th>
							<th scope="col">Address</th>
							<th scope="col">Department</th>
							<th scope="col">Prescription</th>
							<th scope="col">Action</th>
						</tr>
					</thead>
					<tbody>
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
							String search = request.getParameter("searchpatient");

							try {
								connection = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL  + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS);
								statement = connection.createStatement();
								String sql = "SELECT * FROM `patient` WHERE `patient_firstname` = '" + search + "'";

								resultSet = statement.executeQuery(sql);
								while (resultSet.next()) {
						%>

						<tr>
							<th scope="row"><%=resultSet.getString("patient_id")%></th>
							<td><a
								href='patient_profile.jsp?id=<%=resultSet.getString("patient_id")%>'><%=resultSet.getString("patient_firstname")%></a></td>
							<td><%=resultSet.getString("patient_lastname")%></td>
							<td><%=resultSet.getString("address")%></td>
							<td><%=resultSet.getString("department")%></td>
							<td><%=resultSet.getString("prescription")%></td>
							<td><a
								href='editpatient.jsp?id=<%=resultSet.getString("patient_id")%>'>Edit</a>
								| <a
								href='DeletePatient?id=<%=resultSet.getString("patient_id")%>'>Delete</a></td>
						</tr>
					</tbody>
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