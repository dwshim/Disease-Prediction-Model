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

@WebServlet("/Login")
public class Login extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public Login() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}
	
	//Developed in iteration 1
	//Send request to verify user credentials and storing data into session 
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);

		String name = request.getParameter("username");
		String pass = request.getParameter("pass");

		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS); 
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery(
					"select username,password,role from user where username='" + name + "' and password='" + pass + "'");

			if (rs.next()) {
				String role = rs.getString("role");
				HttpSession session = request.getSession();
				session.setAttribute("username", name);
				session.setAttribute("role", role);
				response.sendRedirect("home.jsp");
			} else {
				response.sendRedirect("error.jsp");
			}
			
			stmt.close();
			rs.close();
			conn.close();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
	}

}
