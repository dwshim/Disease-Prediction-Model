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
		<%@ include file="template.jsp"%>
		<!-- /#sidebar-wrapper -->

		<!-- Page Content -->
		<div id="page-content-wrapper">
			<%
				try {
					Class.forName(driverName);
				} catch (ClassNotFoundException e) {
					e.printStackTrace();
				}

				Connection connection = null;
				Statement statement = null;
				ResultSet resultSet = null;
				ResultSet resultSet2 = null;
				int i = 1;

				try {
					connection = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL  + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS);
					statement = connection.createStatement();
					String sql = "SELECT patient_data.patient_id, patient.patient_id, patient.patient_firstname, patient.patient_lastname, patient_data.bmi, patient_data.glucose, patient_data.bloodp, patient_data.pedigree, patient_data.pregnancies"
							+ " FROM patient_data INNER JOIN patient ON patient_data.patient_id = patient.patient_id WHERE patient_data.patient_id = "
							+ request.getParameter("id");
					resultSet = statement.executeQuery(sql);
					if(!resultSet.first()){
						Statement statement2 = null;
						statement2 = connection.createStatement();
						String sql2 = "INSERT INTO patient_data (`patient_id`, `bmi`, `glucose`, `bloodp`, `pregnancies`, `pedigree`) VALUES ("+ request.getParameter("id") + ", 0,0,0,0,0)";
						int f = statement2.executeUpdate(sql2);
						resultSet = statement.executeQuery(sql);
					}
			%>
			<div class="container-fluid">
				<h1 class="mt-4">
					Patient Name:
					<%=resultSet.getString("patient_firstname")%>
					<%=resultSet.getString("patient_lastname")%></h1>
				<form method="POST"
					action="edithealthdata.jsp?id=<%=resultSet.getString("patient_id")%>">
					<table class="table">
						<thead>
							<tr>
								<th scope="col">BMI</th>
								<th scope="col">Glucose Level</th>
								<th scope="col">Blood Pressure</th>
								<th scope="col">Pregnancies</th>
								<th scope="col">Pedigree</th>
							</tr>
						</thead>
						<tbody>
							<tr>

								<td><%=resultSet.getString("bmi")%></td>
								<td><%=resultSet.getString("glucose")%></td>
								<td><%=resultSet.getString("bloodp")%></td>
								<td><%=resultSet.getString("pregnancies")%></td>
								<td><%=resultSet.getString("pedigree")%></td>
							</tr>
						</tbody>

						<%
							} catch (Exception e) {
								e.printStackTrace();
							}

							connection.close();
						%>
					</table>

					<button class="btn btn-primary">Edit Data</button>
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