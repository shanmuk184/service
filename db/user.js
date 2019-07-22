conn = new Mongo();
db = conn.getDB("dev");
cursor = db.user.find();
while(cursor.hasNext()){
   if (cursor.next()){
      printjson(cursor.next());
   }
}
