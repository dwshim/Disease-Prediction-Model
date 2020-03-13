<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%@page import="java.sql.DriverManager"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Statement"%>
<%@page import="java.sql.Connection"%>

<%
	String id = request.getParameter("userId");
	String driverName = "com.mysql.jdbc.Driver";
	String connectionUrl = "jdbc:mysql://localhost:3306/";
	String dbName = "hospital";
	String userId = "root";
	String password = "";
%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Patient Management</title>
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
				<h1 class="mt-4">List of Patient</h1>
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
						<tr>
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
									String sql = "SELECT * FROM patient";

									resultSet = statement.executeQuery(sql);
									while (resultSet.next()) {
							%>
							<th scope="row">
								<%=resultSet.getString("patient_id")%>
							</th>
							<td><a href ='patient_profile.jsp?id=<%=resultSet.getString("patient_id")%>'><%=resultSet.getString("patient_firstname")%></a></td>
							<td><%=resultSet.getString("patient_lastname")%></td>
							<td><%=resultSet.getString("address")%></td>
							<td><%=resultSet.getString("department")%></td>
							<td><%=resultSet.getString("prescription")%></td>
							<td><a href='DeletePatient?id=<%=resultSet.getString("patient_id")%>'>Delete</a></td>
						</tr>
					</tbody>

					<%
						}

						} catch (Exception e) {
							e.printStackTrace();
						}
					%>
				</table>
				<div class="container-login100-form-btn">
					<button class="btn btn-primary" onclick="window.location='addpatient.jsp'">Add Patient</button>
				</div>
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