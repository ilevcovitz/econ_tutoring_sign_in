{%- extends 'full.tpl' -%}

{% block input_group -%}
<div class="input_hidden">
{{ super() }}
</div>
{% endblock input_group %}

{%- block header -%}
{{ super() }}



<style type="text/css">
.input_hidden {
  display: none;
  margin-top: 5px;
}
div.prompt {
display: none;
}
div.output_stderr {
display: none;
}
</style>


{%- endblock header -%}