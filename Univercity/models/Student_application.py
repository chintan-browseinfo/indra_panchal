from odoo import models, fields, api, _

class StudentApplication(models.Model):
    _name = "studentapplication.module"
    _description = "Student application Module"

    name = fields.Char(String='Name',required=True,track_visibility='onchange')
    phone_number = fields.Char(String='Contact Number',required=True,size=10)
    email = fields.Char(String='Email Address')
    address = fields.Text(String='Address')
    birthday = fields.Date(string='Birthday Date', copy=False)
    gender = fields.Selection([
        ('M','Male'),
        ('F','Female')],String='select Gender',required=True)
    degree = fields.Selection([
        ('UG','UG Degree'),
        ('PG','PG Degree')],String='select Degree',default=None)
    education_id = fields.Many2one('education.module',String="Education")
    student_document = fields.One2many('studentdocument.module', 'student_id',String="Student Document")

    @api.multi
    @api.depends("course_id")
    def _compute_student_code(self):
        for o in self:
            o.course_name = o.course_id.course_name

    course_name = fields.Char('course_name',compute=_compute_student_code)
    course_id = fields.Many2one('univercitycourse.module', String="Course")
    student_club_ids = fields.Many2many('univercityclub.module', 'stu_uniclub_rel', 'student_club_id','uniclub_id', string="Club")