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
<title>User Management</title>
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
			<div class="container-fluid">
				<h1 class="mt-4">User Management</h1>
				<table class="table">
					<thead>
						<tr>
							<th scope="col">Employee ID</th>
							<th scope="col">Username</th>
							<th scope="col">Role</th>
							<th scope="col">Title</th>
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
									String sql = "SELECT * FROM user WHERE role != '" + role + "'";

									resultSet = statement.executeQuery(sql);
									while (resultSet.next()) {
							%>
							<th scope="row">
								<%=resultSet.getString("employee_id")%>
							</th>
							<td><%=resultSet.getString("username")%></td>
							<td><%=resultSet.getString("role")%></td>
							<td><%=resultSet.getString("title")%></td>
							<td><a href='editemployee.jsp?id=<%=resultSet.getString("employee_id")%>'>Edit</a> | <a href='DeleteUser?id=<%=resultSet.getString("employee_id")%>'>Delete</a></td>
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
					<button class="btn btn-primary" onclick="window.location='addemployee.jsp'">Add Employee</button>
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