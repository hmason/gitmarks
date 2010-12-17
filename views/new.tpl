<h1 style="text-align: center">store gitmark</h1>

<form method="POST" action="create" class="save">
  %if error:
    <p class="error">
    {{error}}
    </div>
  %end

  <p>
    <label name="url">url</label>
    <input type="text" name="url" value="{{url or ''}}" class="text" />
  </p>

  <p>
    <label name="message">description</label>
    <input type="text" name="message" value="{{message or ''}}" class="text" />
  </p>

  <p>
    <label name="tags">tags</label>
    <input type="text" name="tags" value="{{tags or ''}}" class="text" />
  </p>

  <p>
    <label name="nopush">&nbsp;</label>
    <input type="checkbox" name="nopush" value="1" />
    do not push to the origin server
  </p>

  <p>
    <input type="submit" value="save" class="button">
  </p>

</form>

%rebase layout