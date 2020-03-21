<div class="bg-light border-right" id="sidebar-wrapper">
	<div class="sidebar-heading">Sweet Hospital</div>
	<div class="list-group list-group-flush">
	<a href="home.jsp"
			class="list-group-item list-group-item-action bg-light">Home</a>
		<a href="predictor.jsp"
			class="list-group-item list-group-item-action bg-light">Predictor</a>
		<%
			String role = (String) session.getAttribute("role");
			if (role != null) {
				if (role.equals("System Administrator") || role.equals("Patient Administrator")) {
		%>
		<a href="patient.jsp"
			class="list-group-item list-group-item-action bg-light">Patient List</a>
		<%
			}
				if (role.equals("System Administrator")) {
		%>
		<a href="usermanagement.jsp"
			class="list-group-item list-group-item-action bg-light">User Management </a>
		<%
			}
			}
		%>
		<a href="logout.jsp"
			class="list-group-item list-group-item-action bg-light">Logout</a>
	</div>
</div>
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
			</ul>
		</div>
	</nav>