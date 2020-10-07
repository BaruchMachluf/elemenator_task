-- SQL #1
with emp_salary_rank
as
(
select d.department_name, e.employee_id, e.salary
,row_number() over(partition by d.department_name order by e.salary desc) rank_salary
from employees e
join departments d on e.department_id = d.department_id
)

select t1.department_name
,t1.employee_id
,t1.salary
,(t1.salary - ifnull(t2.salary,0)) as salary_diff_from_second_employee
from emp_salary_rank as t1
left join emp_salary_rank as t1 on t1.employee_id = t2.employee_id
where t1.rank_salary = 1 and t2.rank_salary = 2



-- SQL #2
select 
sum(case when (sv.date between pd.start_date and pd.end_date) then sv.number_of_visitors else 0.0 end)* 1.0  / sum(sv.number_of_visitors) as percent_site_traff_on_promo_dates 
from site_visitors sv
left join promotion_dates pd on sv.site = pd.site

