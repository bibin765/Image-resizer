import { Component } from '@angular/core';
import { HttpClient,HttpResponse } from '@angular/common/http';
import { DomSanitizer} from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'image-resizer';
  selectedFile: File = null;
  imageURL = null;
  resizedDetails = null;
  arrayDetails = null;
  headers = [0,1,2,3];
  buttonSelect = false;
  button25 = false;
  button50 = false;
  localUrl = null;

  constructor(private http: HttpClient,private sanitizer: DomSanitizer){

  }

  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

  button25Select(){
    this.button25 = true;
    this.button50 = false;
    this.localUrl = 'http://localhost:5000/25';
  }

  button50Select(){
    this.button50 = true;
    this.button25 = false;
    this.localUrl = 'http://localhost:5000/50';
  }

  onUpload(){
    const fd = new FormData();
    fd.append('file', this.selectedFile , this.selectedFile.name);
    this.http.post(this.localUrl,fd,{
      responseType: 'blob'
    })
     .subscribe(response => {
        let objectURL = URL.createObjectURL(response);
        this.imageURL=this.sanitizer.bypassSecurityTrustResourceUrl(objectURL);
     });
  }

  ngOnInit(){
    this.http.get('http://localhost:5000').subscribe(
      response => {
        this.arrayDetails = response;
        this.resizedDetails = JSON.stringify(response);
      }
    )
    
  }
}
