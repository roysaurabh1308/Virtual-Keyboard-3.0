
<?php
ini_set('max_execution_time', 0);
set_time_limit(1800);
$vars="";
if(isset($_POST['Vk']))
{
	exec('A: && cd AnaConda\condabin && conda activate myenv && D: && cd/ && cd "Courses\IIIT - CS 3rd Year\Minor\VK" && python Virtual_Keyboard3.0.py');
	$filename = "lol.html"; 
	$file = fopen( $filename, 'r' ); 
	$size = filesize( $filename ); 
	$vars = fread( $file, $size );
}
if(isset($_POST['Wiki']))
{
	header("location:https://en.wikipedia.org/wiki/".$_POST['sval']);
}
if(isset($_POST['Goo']))
{
	header("location:https://www.google.com/search?q=".$_POST['sval']);
}
?>

<style>
input[type=text] {
  width: 60%;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
  background-image: url('https://cdn1.iconfinder.com/data/icons/hawcons/32/698627-icon-111-search-512.png');
  background-position: 10px 10px; 
  background-repeat: no-repeat;
  padding: 12px 20px 12px 40px;
}
.button,i {
  display: inline-block;
  padding: 15px 25px;
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: #fff;
  background-color: #4CAF50;
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px #999;
}

.button:hover,i:hover {background-color: #3e8e41}

.button:active,i:active {
  background-color: #3e8e41;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}

 

</style>
<center  style='margin-top:30vh'>
<div >
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<h1>Demo1: Search Using Virtual Keyboard....</h1>
<form method="POST" action="/">
<input id="i1" type="text" name="sval" value="<?php echo $vars; ?>"/>
<button style="font-size:24px" name="Vk" onclick="this.form.submit()"><i class="fa fa-camera"></i></button><br><br><br>
<input class="button" type="submit" name="Wiki" value="Search WikiPedia"/>
<input class="button" type="submit" name="Goo" value="Search Google"/>
</form>

</div>
<center>