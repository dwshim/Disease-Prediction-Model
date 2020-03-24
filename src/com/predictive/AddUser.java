package com.predictive;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/AddUser")
public class AddUser extends HttpServlet{
	
	private static final long serialVersionUID = 1L;

	public AddUser
	() {
		super();
	}
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	//Developed in iteration 4
	//Establish connection with mySQL to create a new record
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);

		String username = request.getParameter("username");
		String pass = request.getParameter("password");
		String role = request.getParameter("role");
		String title = request.getParameter("title");

		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/hospital", "root", "");
			Statement stmt = conn.createStatement();
			int i = stmt.executeUpdate(
					"INSERT INTO `user`(`username`, `password`, `role`, `title`) VALUES ('"
							+ username + "','" + pass + "','" + role + "','" + title 
							+ "')");
			if (i > 0) {
				response.sendRedirect("usermanagement.jsp");
			} else {
				response.sendRedirect("error.jsp");
			}
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
