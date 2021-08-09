import datetime

from projectApp.models import Student, LearningObjective, Child


class StudentAdminManager:

    def updateProfileReviewed(self, stud_id):
        if stud_id:
            Student.objects.filter(id=stud_id).update(status='Reviewed')
            return True
        return False

    def updateNotify(self, stud_id):
        if stud_id:
            Student.objects.filter(id=stud_id).update(status='Notify')
            return True
        return False

    def import_csv(self, obj):
        """
        To write data from csv to student model.
        :param request:
        :return:
        """
        if obj:
            for line in obj:
                if line:
                    fields = line.split(",")
                    try:
                        is_exist = Student.objects.get(id=fields[0])
                    except Exception as e:
                        is_exist = None
                    if is_exist is None:
                        Student.objects.create(
                            id=fields[0].strip(),
                            stud_id=fields[1].strip(),
                            fname=fields[2].strip(),
                            lname=fields[3].strip(),
                            gender=fields[4].strip(),
                            age=fields[5].strip(),
                            status='Created'
                        )
                    else:
                        stud_obj = Student.objects.get(id=fields[0])
                        Student.objects.filter(id=fields[0]).update(
                            stud_id=fields[1].strip(),
                            fname=fields[2].strip(),
                            lname=fields[3].strip(),
                            gender=fields[4].strip(),
                            age=fields[5].strip(),
                            status=stud_obj.status

                        )
            return True
        return False

class ChildManager:

    def csv_import(self, obj):

        if obj:
            for line in obj:
                if line:
                    fields = line.split(",")
                    dict_val = {fields[6].split(":")[0]: fields[6].split(":")[1],
                                fields[7].split(":")[0]: fields[7].split(":")[1],
                                fields[8].split(":")[0]: fields[8].split(":")[1],
                                fields[9].split(":")[0]: fields[9].split(":")[1],
                                fields[10].split(":")[0]: fields[9].split(":")[1],
                                fields[11].split(":")[0]: fields[11].split(":")[1],
                                fields[12].split(":")[0]: fields[12].split(":")[1]}
                    code_list = [fields[6].split(":")[0], fields[7].split(":")[0], fields[8].split(":")[0],
                                 fields[9].split(":")[0], fields[10].split(":")[0], fields[11].split(":")[0],
                                 fields[12].split(":")[0]]
                    for k, v in dict_val.items():
                        try:
                            if k and v:
                                try:
                                    is_exist = LearningObjective.objects.get(code=k)
                                except Exception as e:
                                    is_exist = None

                                if not is_exist:
                                    LearningObjective.objects.get_or_create(code=k, description=v, status=1,
                                                                            added_on=str(datetime.datetime.now()),
                                                                            updated_on=str(datetime.datetime.now()))
                        except Exception as e:
                            print(e)
                    try:
                        learning_obj = LearningObjective.objects.filter(code__in=code_list)
                        child_instance = Child.objects.get_or_create(
                            name=fields[2].strip(),
                            parent_name='NA',
                            mobile=fields[13].strip(),
                            email=fields[1].strip(),
                            grade='NA',
                            teacher_allocated=fields[3].strip(),
                            current_teacher='NA',
                            sales_manager='NA',
                            lsq_id='NA',
                            last_active_date=str(datetime.datetime.now()),
                            ptm_status=0,
                            last_ptm_date=str(datetime.datetime.now()),
                            batch_name='NA',
                            course_name=fields[5].strip(),
                            sessions_credited=fields[14].strip(),
                            start_date=str(fields[4]),
                            status=1,
                            added_on=str(datetime.datetime.now()),
                            updated_on=str(datetime.datetime.now()),
                            timestamp=str(fields[0].strip()),
                        )
                        is_exist = Child.objects.get(name=fields[2])
                        if not is_exist:
                            child_instance.learning_objective.set(tuple(learning_obj))
                    except Exception as e:
                        print(e)
            return True
        return False