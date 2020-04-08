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
<title>Predictor</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Bootstrap core CSS -->
<link href="css/bootstrap.min.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="css/simple-sidebar.css" rel="stylesheet">
</head>
<body>
	<%
		String id = request.getParameter("id");
		String name = (String) session.getAttribute("username");
		String driverName = "com.mysql.jdbc.Driver";
		String message = (String) request.getAttribute("result");
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
				<h1 class="mt-4">Predictor</h1>
				<%
					if (id != null) {
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
							connection = DriverManager.getConnection(
									"jdbc:mysql://" + DatabaseInfo.DB_URL + "/" + DatabaseInfo.DB_NAME + "",
									DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS);
							statement = connection.createStatement();
							String sql = "SELECT * FROM `patient_data` WHERE `patient_id` = '" + request.getParameter("id")
									+ "'";

							resultSet = statement.executeQuery(sql);
							while (resultSet.next()) {
				%>
				<form method="POST" action="SendJSON">
					<div class="form-group">
						<input type="text" class="form-control" id="bmi" name="bmi"
							placeholder="Concave Points Mean" value="<%=resultSet.getString("bmi")%>"
							required>
					</div>

					<div class="form-group">
						<input type="text" class="form-control" name="glucose"
							id="glucose" placeholder="Radius Worst"
							value="<%=resultSet.getString("glucose")%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="bp" name="bp"
							placeholder="Perimeter Worst"
							value="<%=resultSet.getString("bloodp")%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pregnancies"
							name="pregnancies" placeholder="Area Worst"
							value="<%=resultSet.getString("pregnancies")%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pedigree"
							name="pedigree" placeholder="Concave Points Worst"
							value="<%=resultSet.getString("pedigree")%>" required>
					</div>

					<div class="form-group">
						<p>
							Result:

							<%
							if(message!=null){
							if (message.equals("[1]")) {
											out.print("malignant");
										} else if (message.equals("[0]")) {
											out.print("benign");
										} else {
											out.print("null");
										}
							}
						%>
						</p>
					</div>

					<button class="btn btn-primary">Submit</button>
				</form>

				<%
					}
						} catch (Exception e) {
							e.printStackTrace();
						}

						connection.close();
					} else {
						String a = (String) request.getAttribute("area_worst");
						String b = (String) request.getAttribute("radius_worst");
						String c = (String) request.getAttribute("perimeter_worst");
						String d = (String) request.getAttribute("concave_points_mean");
						String e = (String) request.getAttribute("concave_points_worst");
						if(a == null || b == null || c == null || d == null || e == null) {
							a = "";
							b = "";
							c = "";
							d = "";
							e = "";
						}
				%>

				<form method="POST" action="SendJSON">
					<div class="form-group">
						<input type="text" class="form-control" id="bmi" name="bmi"
							placeholder="Concave Points Mean" value="<%=a%>" required>
					</div>

					<div class="form-group">
						<input type="text" class="form-control" name="glucose"
							id="glucose" placeholder="Radius Worst" value="<%=b%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="bp" name="bp"
							placeholder="Perimeter Worst" value="<%=c%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pregnancies"
							name="pregnancies" placeholder="Area Worst" value="<%=d%>" required>
					</div>
					<div class="form-group">
						<input type="text" class="form-control" id="pedigree"
							name="pedigree" placeholder="Concave Points Worst" value="<%=e%>" required>
					</div>

					<div class="form-group">
						<p>
							Result:
							<%
							if (message != null){
							if (message.equals("[1]")) {
									out.print("malignant");
								} else if (message.equals("[0]")) {
									out.print("benign");
								} else {
									out.print("null");
								}
							}
						%>
						</p>
					</div>

					<button class="btn btn-primary">Submit</button>
				</form>

				<%
					}
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