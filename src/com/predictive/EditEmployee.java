package com.predictive;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/EditEmployee")
public class EditEmployee extends HttpServlet{
	private static final long serialVersionUID = 1L;

	public EditEmployee() {
		super();
		// TODO Auto-generated constructor stub
	}
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);

		String username = request.getParameter("username");
		String password = request.getParameter("password");
		String role = request.getParameter("role");
		String title = request.getParameter("title");
		String id = request.getParameter("employeeid");

		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/hospital", "root", "");
			Statement stmt = conn.createStatement();
			int i = stmt.executeUpdate(
					"UPDATE `user` SET `username` = '" + username + "'" + "," 
			+ "`password` = '" + password + "'" + "," 
							+ "`role` = '" + role + "'" + "," 
			+ "`title` = '" + title + "'" 
			+ "WHERE employee_id='" + id +"'");
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
