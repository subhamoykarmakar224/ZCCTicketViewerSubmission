<html>
  <head>
    <title>Zendesk Ticket Viewer</title>
    <link href="/css/main.css" rel="stylesheet">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  </head>
  <body class="container">
      <h2>Welcome! {{name}}  ({{role}})</h2>
      {{error}}
      <p>
      <h3>Ticket Lists (Total: {{ ticket_count }})</h3>
      <p>{{cur_page}} of {{page_count}} Pages</p>
      <p>
          <a href="/{{cur_page - 1}}">Prev</a>&nbsp;&nbsp;&nbsp;&nbsp;
          <a href="/{{cur_page + 1}}">Next</a>
      </p>
      <table class="table table-striped">
          <thead>
            <tr>
                <th>ID</th>
                <th>Requested</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Subject</th>
            </tr>
          </thead>
          <tbody>
            % for ticket in tickets:
            <tr>
              <td>{{ ticket['id'] }}</td>
              <td>{{ ticket['created_at'] }}</td>
              <td>{{ ticket['status'] }}</td>
              <td>{{ ticket['priority'] }}</td>
              <td>{{ ticket['subject'] }}</td>
            </tr>
            % end
          </tbody>
      </table>
      </p>
  </body>
</html>
