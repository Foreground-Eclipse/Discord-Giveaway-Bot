import sqlite3
from pathlib import Path


queryGiveaway = "CREATE TABLE if not exists giveaway (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, timeout text NOT NULL, initiator text, messageID text,channelID text,guildID text, status text)"
queryWinners = "CREATE TABLE if not exists participants (id integer primary key autoincrement not null, discordid text not null, giveawayID integer, foreign key(giveawayID) references giveaway(id))"

connPath = f"{Path.cwd().resolve()}/db/giveaways.db"


try:
    sqlite_connection = sqlite3.connect(connPath)
    cursor = sqlite_connection.cursor()

    cursor.execute(queryGiveaway)
    cursor.execute(queryWinners)
    sqlite_connection.commit()
except sqlite3.Error as err:
    print(f"Sqlite returned a mistake during making the tables, {err}")
    sqlite_connection.rollback()
finally:
    cursor.close() 
    sqlite_connection.close()  



def insertGiveaways(timeout: str, initiator: str, messageID: str, channelID: str, guildID: str):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("insert into giveaway (timeout,  initiator, messageID,channelID,guildID,status) VALUES (?,?,?,?,?,?)", (timeout, initiator, messageID,channelID,guildID,"ONGOING"))
        sqlite_connection.commit()

        return None

    except sqlite3.Error as error:
        print("SQLite error in insertGiveaways", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()


def insertParticipant(discordid: str, giveawayID:int):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("insert into participants (discordid, giveawayid) VALUES (?,?)", (discordid, giveawayID))
        sqlite_connection.commit()

        return None

    except sqlite3.Error as error:
        print("SQLite error in insertParticipant", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()


def getGiveawayID(messageID: str):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("select ID from giveaway where messageID = ?", (messageID,))
        messageID = cursor.fetchall()

        return str([message for message in messageID[0]][0])

    except sqlite3.Error as error:
        print("SQLite error in getGiveawayID", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()

def checkIfAlreadyParticipate(discordID : int, giveawayID: str):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("select count(*) from participants where discordid = ? and giveawayid = ?", (str(discordID),giveawayID))
        count = cursor.fetchall()

        return [message for message in count[0]][0]

    except sqlite3.Error as error:
        print("SQLite error in checkIfAlreadyparticipate", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()

def getAllGiveawaysTimeout():
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("select timeout, messageID, channelID, guildID from giveaway where status = ?",("ONGOING",))
        count = cursor.fetchall()

        return [message for message in count]

    except sqlite3.Error as error:
        print("SQLite error in insertGetAllGivewawaysaTimeouts", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()






def updateGiveawayStatus(messageID: str):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("update giveaway set status = ? where messageID = ?", ("ENDED", messageID))
        sqlite_connection.commit()

        return None

    except sqlite3.Error as error:
        print("SQLite error in updateGiveawayStatus", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()




def getAllParticipants(messageID: str):
    try:
        sqlite_connection = sqlite3.connect(connPath)
        cursor = sqlite_connection.cursor()
        
        cursor.execute("select discordid from participants where giveawayID = ?", (getGiveawayID(messageID),))
        count = cursor.fetchall()

        return [message[0] for message in count]

    except sqlite3.Error as error:
        print("SQLite error in getAllParticipants", error)
        return error
    
    finally:
        cursor.close()
        sqlite_connection.close()




