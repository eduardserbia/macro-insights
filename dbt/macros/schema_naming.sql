{% macro generate_schema_name(custom_schema_name, node) %}
    {# 
      If a custom schema is provided in dbt_project.yml (+schema),
      use it AS-IS (no prefix with target.schema).
      Otherwise fallback to target.schema.
    #}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name }}
    {%- endif -%}
{% endmacro %}
