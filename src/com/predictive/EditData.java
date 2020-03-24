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

@WebServlet("/EditData")
public class EditData extends HttpServlet{
	private static final long serialVersionUID = 1L;

	public EditData() {
		super();
	}
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	//Developed in iteration 4
	//Establish connection with mySQL to edit record
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);

		String bmi = request.getParameter("bmi");
		String glucose = request.getParameter("glucose");
		String bp = request.getParameter("bp");
		String pregnancies = request.getParameter("pregnancies");
		String pedigree = request.getParameter("pedigree");
		String id = request.getParameter("patientid");

		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/hospital", "root", "");
			Statement stmt = conn.createStatement();
			int i = stmt.executeUpdate(
					"UPDATE `patient_data` SET `bmi` = '" + bmi + "'" + "," 
			+ "`glucose` = '" + glucose + "'" + "," 
							+ "`bloodp` = '" + bp + "'" + "," 
			+ "`pregnancies` = '" + pregnancies + "'" + "," 
							+ "`pedigree` = '" + pedigree + "'" 
			+ "WHERE patient_id='" + id +"'");
			if (i > 0) {
				response.sendRedirect("patient_profile.jsp?id=" + id);
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
