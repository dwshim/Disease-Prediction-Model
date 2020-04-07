<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page import="java.util.*"%>
<%@ page import="com.google.gson.Gson"%>
<%@ page import="com.google.gson.JsonObject"%>
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
	<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
	<%
		String name = (String) session.getAttribute("username");
		if (name == null) {
			response.sendRedirect("login.jsp");
		}
		Gson gsonObj = new Gson();
		Map<Object, Object> map = null;
		HashMap<String, String> hm = new HashMap<String, String>();

		List<Map<Object, Object>> list = new ArrayList<Map<Object, Object>>();
	%>

	<div class="d-flex" id="wrapper">

		<!-- Sidebar -->
		<%@ include file="template.jsp"%>
		<!-- /#sidebar-wrapper -->

		<!-- Page Content -->
		<div id="page-content-wrapper">


			<div class="container-fluid">

				<div id="chartContainer" style="height: 450px; width: 100%;"></div>

				<%
					/* try {
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
						String sql = "SELECT department FROM `patient`";
					
						resultSet = statement.executeQuery(sql);
						int count = 0;
						while (resultSet.next()) {
							count++;
							if (hm.containsKey(resultSet.getString("department"))) {
								hm.put(resultSet.getString("department"), hm.get(resultSet.getString("department")) + 1);
							} else {
								hm.put(resultSet.getString("department"), 1.0);
							}
						}
					
						for (Map.Entry<String, Double> z : hm.entrySet()) {
							map = new HashMap<Object, Object>();
							map.put("label", z.getKey());
							map.put("y", Math.round(z.getValue() / count * 100));
							list.add(map);
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
					
					connection.close();
					*/
					map = new HashMap<Object, Object>();
					map.put("label", "Benign");
					map.put("y", 30);
					list.add(map);
					map = new HashMap<Object, Object>();
					map.put("label", "Malignant");
					map.put("y", 12);
					list.add(map);
					String dataPoints = gsonObj.toJson(list);
				%>

				<!DOCTYPE HTML>
				<html>

<script type="text/javascript">
	window.onload = function() {

		var chart = new CanvasJS.Chart("chartContainer", {
			animationEnabled : true,
			title : {
				text : "Prediction result overview"
			},
			axisX : {
				title : "Condition"
			},
			data : [ {
				type : "column",
				dataPoints :
<%out.print(dataPoints);%>
	} ]
		});
		chart.render();

	}
</script>

				</html>