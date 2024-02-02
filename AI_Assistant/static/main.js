var log=[]
var chatFrame;
var id=""
var counter=0;
var system=""
var s2tFrame;
var user=""

            const audioPlayer = new AudioPlayer("../static/dist2");

			window.onload = function () {
			    s2tFrame=document.getElementById('myquestion')
			    audio = document.getElementById('audioPlayer');
			    if (document.getElementById('current_user'))
			        user = document.getElementById('current_user').innerHTML;

			    id=document.getElementById('id')

				document.getElementById('stopButton').disabled=true

				chatFrame=document.getElementById("parent")

				setTimeout(function(){
					chatFrame.scrollTop = chatFrame.scrollHeight;
				},0);
                // load chat history
				fetch('/load_msg',{
                    method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({app_type: id.innerHTML,current_user:user}),
				}).then(response => {
                        console.log(response)

                        const reader = response.body.getReader();
                        const decoder = new TextDecoder('utf-8');
                        let buffer = '';

                        function processStreamResult(result2) {
                            const chunk = decoder.decode(result2.value, { stream: !result2.done });
                            buffer += chunk;

                            const lines = buffer.split('\n');
                            buffer = lines.pop();

                            lines.forEach(line => {
                                if (line.trim().length > 0) {

                                  var obj=JSON.parse(line)

                                  log.push({"role": obj.msg_sender, "content": obj.msg_content});

                                  addElementDiv(obj.msg_content,parseInt(obj.msg_id),obj.msg_sender);
                                  counter=parseInt(obj.msg_id)

                                  console.log("--------------------------------------------")
                                  chatFrame.scrollTop = chatFrame.scrollHeight;
                                }
                            });

                            if (!result2.done) {
                                return reader.read().then(processStreamResult);
                            }
                        }

                        return reader.read().then(processStreamResult);
                    })
						.catch(error => {
							console.error('Error:', error);
						});

			}

			var stop=1
			function chat(opt){
			// send message
			    if(document.getElementById('tag').innerHTML=="Register"){
                    alert("Please log in to proceed");
                    return;
                }
				tmp_question=$("#myquestion").val()
				system=$("#system").val()
				if (tmp_question.trim()=="")
					return

				document.getElementById('sendButtonArea').hidden=true
				document.getElementById('stopButtonArea').hidden=false

				document.getElementById('stopButton').disabled=false
				stop=0
				document.getElementById('myquestion').disabled="disabled"
				document.getElementById('sendButton').disabled="disabled"
				document.getElementById('clearButton').disabled=true

				log.push({"role": "user", "content": tmp_question});
				document.getElementById('myquestion').value="";
				counter+=1
				addElementDiv(tmp_question,counter,"user");
				setTimeout(function(){
					chatFrame.scrollTop = chatFrame.scrollHeight;
				},0);

//				localStorage.setItem(id.innerHTML+user,JSON.stringify(log))
				var n = 5
				//$("#chatResponse").text(log);
				content=""
				let history_arr=[]
				let history_count=0
				for (var i=log.length-1;i>=0;i--){
				    if (log[i].content){
				        history_arr.unshift(log[i])
				        history_count+=1
				    }
                    if (history_count>=n)
                        break
				}
//				console.log(history_arr)
				fetch('/chat', {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({app_type: id.innerHTML, message_id:counter,current_user:user,option:opt,system:system,question:tmp_question,history:JSON.stringify(history_arr)}),
				}).then(response => {
					const reader = response.body.getReader();
					const decoder = new TextDecoder('utf-8');
					let buffer = '';

                    counter+=1
					addElementDiv("",counter,"assistant");
					var show=document.getElementById('div'+counter.toString())

					function processStreamResult(result2) {
						const chunk = decoder.decode(result2.value, { stream: !result2.done });
						buffer += chunk;

						const lines = buffer.split('\n');
						buffer = lines.pop();

						lines.forEach(line => {
							if (line.trim().length > 0) {

								if(stop==1){

								}else{
									var obj=JSON.parse(line)
									var obj1=obj.delta
									var obj2=obj.finish_reason
									if (obj2!=null){
										log.push({"role": "assistant", "content": content});
//										localStorage.setItem(id.innerHTML+user,JSON.stringify(log))
										document.getElementById('myquestion').disabled=false
										document.getElementById('sendButton').disabled=false
										document.getElementById('clearButton').disabled=false
										document.getElementById('stopButton').disabled=true
										document.getElementById('sendButtonArea').hidden=false
										document.getElementById('stopButtonArea').hidden=true
									} else if(obj1!=null){
										content += obj1
										show.innerHTML = content;
										//console.log(obj1);

										chatFrame.scrollTop = chatFrame.scrollHeight;
									}
									//console.log(line);
								}

							}
						});

						if (!result2.done && stop==0) {
							return reader.read().then(processStreamResult);
						}
					}

					return reader.read().then(processStreamResult);
				})
						.catch(error => {
							console.error('Error:', error);
						});
			}
			function abortStream(opt){
				stop=1
				$.ajax({
					url: "/abort",
					type: "POST",
					data: {
					    current_user:user,
						option: opt
					},
					dataType: "json",
					success: function(response) {
					}
				});
				log.push({"role": "assistant", "content": content});
//				localStorage.setItem(id.innerHTML+user,JSON.stringify(log))
				document.getElementById('myquestion').disabled=false
				document.getElementById('sendButton').disabled=false
				document.getElementById('clearButton').disabled=false
				document.getElementById('stopButton').disabled=true
				document.getElementById('sendButtonArea').hidden=false
				document.getElementById('stopButtonArea').hidden=true
			}
			function clearChat(){
				log=[]
				counter=0
				var pObjs = chatFrame.childNodes;
				for (var i = pObjs.length - 1; i >= 0; i--) {
					chatFrame.removeChild(pObjs[i]);
				}
				$.ajax({
                        url: "/del_all",
                        type: "POST",
                        data: {
                            user_name: user,
                            app_type: id.innerHTML,
                        },
                        dataType: "json",
                        success: function (res) {
                        }
                    });
			}
            function msg_to_process(msg_id){
            // send message for text-to-speech and play the audio
                console.log(document.getElementById("div"+msg_id).innerHTML)
                fetch('/play4', {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({current_user:user, msg: document.getElementById("div"+msg_id).innerHTML,opt:document.getElementById("voice_opt").innerHTML}),
				}).then(response => {
//				    console.log(response)
                    audioPlayer.start({
                        autoPlay: true,
                        sampleRate: 24000,
                      });
					const reader = response.body.getReader();
                    return reader.read().then(function process({ done, value }) {
                      if (done) {
                        console.log('Stream finished');
                        return;
                      }

                      console.log('Received data chunk', value);
                      audioPlayer.postMessage({
                        type: "base64",
                        data: uint8arrayToBase64(value),
                        isLastData: 0,
                      });

                      return reader.read().then(process);
                    });

                  }).catch(console.error);
//                  audioPlayer.play();
                  audioPlayer.stop();
			}
			function uint8arrayToBase64(u8Arr) {
                let CHUNK_SIZE = 1024; //arbitrary number
                let index = 0;
                let length = u8Arr.length;
                let result = '';
                let slice;
                while (index < length) {
                    slice = u8Arr.subarray(index, Math.min(index + CHUNK_SIZE, length));
                    result += String.fromCharCode.apply(null, slice);
                    index += CHUNK_SIZE;
                }
                return btoa(result);
            }
            function addElementDiv(message,counter,speaker){
            // when new message is sent/received add a block to show the new message
				var parent = document.getElementById("parent")
				if (parent==null)
					console.log("empty")
				let div_0 = document.createElement("div")
				div_0.setAttribute("class","clearfix")
				div_0.setAttribute("id","div_0"+counter.toString())

				let div0 = document.createElement("div")
				let div00 = document.createElement("br")
				let div01 = document.createElement("br")
				let div1 = document.createElement("div")

				div0.setAttribute("id","div0"+counter.toString())
				div00.setAttribute("id","div00"+counter.toString())
				div01.setAttribute("id","div01"+counter.toString())
				div1.setAttribute("id","div"+counter.toString())

				div1.setAttribute("onclick","msg_to_process("+counter.toString()+")")
				div1.addEventListener("contextmenu", function(event) {
                  event.preventDefault();
//                  alert(counter.toString());
                    var isbool = confirm('Are you sure you wanna delete this message?');
                    if(isbool == true){
                        console.log(counter.toString()+" deleted");
                        parent.removeChild(div_0)
				        parent.removeChild(div0)
				        parent.removeChild(div00)
				        parent.removeChild(div1)
				        parent.removeChild(div01)

                        $.ajax({
                            url: "/del_msg",
                            type: "POST",
                            data: {
                                user_name: user,
                                app_type: id.innerHTML,
                                message_id:counter,
                            },
                            dataType: "json",
                            success: function (res) {
                            }
                        });

                    }else{
                        console.log('cancelled');
                    }
                });

				div1.style.maxWidth = "250px"
				div1.style.backgroundColor = "#90EE90";
				div1.style.border = "1px solid black";
				div1.style.textAlign = "left";
				div1.style.padding = "2px"
				div1.style.whiteSpace = "pre-line"
				div1.style.boxShadow = "1px 1px 1px 2px gray";

				if (speaker==="user"){
					div0.style.float = "right";
					div00.style.float = "right";
					div1.style.float = "right";
				}
				else{
					div0.style.float = "left";
					div00.style.float = "left";
					div1.style.float = "left";
				}
				div1.style.borderRadius = "5px";
				div0.innerHTML=speaker;
				div1.innerHTML=message;

				parent.appendChild(div_0)
				parent.appendChild(div0)
				parent.appendChild(div00)
				parent.appendChild(div1)
				parent.appendChild(div01)
			}
			function font_size_set(size){
			    document.getElementById("parent").style.fontSize=size.toString()+"px"
			}
			function voice_opt_set(opt){
			    document.getElementById("voice_opt").innerHTML=opt
			}