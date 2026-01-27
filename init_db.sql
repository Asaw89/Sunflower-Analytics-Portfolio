-- Sample data for Zip Listen Analytics

-- Sample listen events
INSERT INTO listen_events (artist, song, duration, userId, state, level, genre, timestamp) VALUES
-- Pop music across regions
('Taylor Swift', 'Anti-Hero', 202.5, 'user001', 'NY', 'paid', 'Pop', NOW() - INTERVAL '1 day'),
('Taylor Swift', 'Lavender Haze', 207.3, 'user002', 'CA', 'free', 'Pop', NOW() - INTERVAL '2 days'),
('Ed Sheeran', 'Shape of You', 233.7, 'user003', 'TX', 'paid', 'Pop', NOW() - INTERVAL '1 day'),
('Ariana Grande', 'Positions', 172.8, 'user004', 'FL', 'paid', 'Pop', NOW() - INTERVAL '3 days'),
('The Weeknd', 'Blinding Lights', 200.1, 'user005', 'IL', 'free', 'Pop', NOW() - INTERVAL '1 day'),

-- Hip-Hop/Rap
('Drake', 'One Dance', 173.4, 'user006', 'GA', 'paid', 'Hip-Hop', NOW() - INTERVAL '2 days'),
('Kendrick Lamar', 'HUMBLE.', 177.0, 'user007', 'NY', 'paid', 'Hip-Hop', NOW() - INTERVAL '1 day'),
('Post Malone', 'Circles', 215.2, 'user008', 'CA', 'free', 'Hip-Hop', NOW() - INTERVAL '4 days'),
('Travis Scott', 'SICKO MODE', 312.8, 'user009', 'WA', 'paid', 'Hip-Hop', NOW() - INTERVAL '2 days'),
('Cardi B', 'WAP', 187.6, 'user010', 'PA', 'free', 'Hip-Hop', NOW() - INTERVAL '1 day'),

-- Rock
('Imagine Dragons', 'Believer', 204.3, 'user011', 'OH', 'paid', 'Rock', NOW() - INTERVAL '3 days'),
('Coldplay', 'Yellow', 267.4, 'user012', 'MA', 'paid', 'Rock', NOW() - INTERVAL '1 day'),
('Queen', 'Bohemian Rhapsody', 354.8, 'user013', 'MI', 'free', 'Rock', NOW() - INTERVAL '2 days'),
('AC/DC', 'Back in Black', 255.1, 'user014', 'AZ', 'paid', 'Rock', NOW() - INTERVAL '1 day'),
('Foo Fighters', 'Everlong', 250.5, 'user015', 'CO', 'paid', 'Rock', NOW() - INTERVAL '3 days'),

-- Country
('Luke Combs', 'Beautiful Crazy', 193.2, 'user016', 'TN', 'paid', 'Country', NOW() - INTERVAL '1 day'),
('Morgan Wallen', 'Wasted On You', 176.4, 'user017', 'NC', 'free', 'Country', NOW() - INTERVAL '2 days'),
('Carrie Underwood', 'Before He Cheats', 199.8, 'user018', 'KY', 'paid', 'Country', NOW() - INTERVAL '1 day'),
('Chris Stapleton', 'Tennessee Whiskey', 282.1, 'user019', 'SC', 'free', 'Country', NOW() - INTERVAL '4 days'),
('Kane Brown', 'Heaven', 175.3, 'user020', 'AL', 'paid', 'Country', NOW() - INTERVAL '2 days'),

-- Electronic
('Daft Punk', 'Get Lucky', 248.2, 'user021', 'OR', 'paid', 'Electronic', NOW() - INTERVAL '1 day'),
('Calvin Harris', 'Summer', 222.9, 'user022', 'NV', 'free', 'Electronic', NOW() - INTERVAL '3 days'),
('Marshmello', 'Happier', 213.7, 'user023', 'WI', 'paid', 'Electronic', NOW() - INTERVAL '2 days'),
('Avicii', 'Wake Me Up', 247.3, 'user024', 'MN', 'paid', 'Electronic', NOW() - INTERVAL '1 day'),
('Zedd', 'Stay', 210.5, 'user025', 'VA', 'free', 'Electronic', NOW() - INTERVAL '2 days'),

-- R&B
('Beyonce', 'Halo', 261.8, 'user026', 'MD', 'paid', 'R&B', NOW() - INTERVAL '1 day'),
('The Weeknd', 'Save Your Tears', 215.5, 'user027', 'NJ', 'paid', 'R&B', NOW() - INTERVAL '3 days'),
('Bruno Mars', 'Just the Way You Are', 220.8, 'user028', 'CT', 'free', 'R&B', NOW() - INTERVAL '2 days'),
('Alicia Keys', 'Fallin', 209.4, 'user029', 'RI', 'paid', 'R&B', NOW() - INTERVAL '1 day'),
('John Legend', 'All of Me', 269.3, 'user030', 'DE', 'paid', 'R&B', NOW() - INTERVAL '2 days'),

-- More recent streams for rising artists calculation
('NewArtist1', 'Viral Song', 180.0, 'user031', 'CA', 'paid', 'Pop', NOW() - INTERVAL '1 hour'),
('NewArtist1', 'Viral Song', 180.0, 'user032', 'NY', 'paid', 'Pop', NOW() - INTERVAL '2 hours'),
('NewArtist1', 'Viral Song', 180.0, 'user033', 'TX', 'free', 'Pop', NOW() - INTERVAL '3 hours'),
('NewArtist1', 'Viral Song', 180.0, 'user034', 'FL', 'paid', 'Pop', NOW() - INTERVAL '4 hours'),
('NewArtist1', 'Another Hit', 195.0, 'user035', 'IL', 'paid', 'Pop', NOW() - INTERVAL '5 hours'),

-- Historical streams for the same artist (for growth calculation)
('NewArtist1', 'Viral Song', 180.0, 'user036', 'CA', 'free', 'Pop', NOW() - INTERVAL '10 days'),
('NewArtist1', 'Another Hit', 195.0, 'user037', 'NY', 'paid', 'Pop', NOW() - INTERVAL '11 days'),

-- More top artists data
('Taylor Swift', 'Shake It Off', 219.0, 'user038', 'CA', 'paid', 'Pop', NOW() - INTERVAL '1 day'),
('Taylor Swift', 'Blank Space', 231.0, 'user039', 'NY', 'paid', 'Pop', NOW() - INTERVAL '2 days'),
('Drake', 'Hotline Bling', 267.0, 'user040', 'TX', 'paid', 'Hip-Hop', NOW() - INTERVAL '1 day'),
('Drake', 'Gods Plan', 198.0, 'user041', 'FL', 'free', 'Hip-Hop', NOW() - INTERVAL '2 days'),
('Ed Sheeran', 'Perfect', 263.0, 'user042', 'GA', 'paid', 'Pop', NOW() - INTERVAL '1 day'),
('The Weeknd', 'Starboy', 230.0, 'user043', 'WA', 'paid', 'Pop', NOW() - INTERVAL '3 days');

-- Sample auth events
INSERT INTO auth_events (success, userId, state, timestamp) VALUES
(true, 'user001', 'NY', NOW() - INTERVAL '1 day'),
(true, 'user002', 'CA', NOW() - INTERVAL '2 days'),
(true, 'user003', 'TX', NOW() - INTERVAL '1 day'),
(false, 'user044', 'FL', NOW() - INTERVAL '3 days'),
(true, 'user004', 'FL', NOW() - INTERVAL '3 days'),
(true, 'user005', 'IL', NOW() - INTERVAL '1 day'),
(true, 'user006', 'GA', NOW() - INTERVAL '2 days'),
(false, 'user045', 'NY', NOW() - INTERVAL '1 day'),
(true, 'user007', 'NY', NOW() - INTERVAL '1 day'),
(true, 'user008', 'CA', NOW() - INTERVAL '4 days'),
(true, 'user009', 'WA', NOW() - INTERVAL '2 days'),
(true, 'user010', 'PA', NOW() - INTERVAL '1 day');

-- Sample status change events (subscription level changes)
INSERT INTO status_change_events (level, userId, state, timestamp) VALUES
-- Paid users
('paid', 'user001', 'NY', NOW() - INTERVAL '30 days'),
('paid', 'user003', 'TX', NOW() - INTERVAL '45 days'),
('paid', 'user004', 'FL', NOW() - INTERVAL '20 days'),
('paid', 'user006', 'GA', NOW() - INTERVAL '60 days'),
('paid', 'user007', 'NY', NOW() - INTERVAL '15 days'),
('paid', 'user009', 'WA', NOW() - INTERVAL '25 days'),
('paid', 'user011', 'OH', NOW() - INTERVAL '40 days'),
('paid', 'user012', 'MA', NOW() - INTERVAL '35 days'),
('paid', 'user014', 'AZ', NOW() - INTERVAL '50 days'),
('paid', 'user015', 'CO', NOW() - INTERVAL '28 days'),
('paid', 'user016', 'TN', NOW() - INTERVAL '32 days'),
('paid', 'user018', 'KY', NOW() - INTERVAL '22 days'),
('paid', 'user020', 'AL', NOW() - INTERVAL '38 days'),
('paid', 'user021', 'OR', NOW() - INTERVAL '42 days'),
('paid', 'user023', 'WI', NOW() - INTERVAL '18 days'),
('paid', 'user024', 'MN', NOW() - INTERVAL '55 days'),
('paid', 'user026', 'MD', NOW() - INTERVAL '48 days'),
('paid', 'user027', 'NJ', NOW() - INTERVAL '33 days'),
('paid', 'user029', 'RI', NOW() - INTERVAL '27 days'),
('paid', 'user030', 'DE', NOW() - INTERVAL '44 days'),

-- Free users
('free', 'user002', 'CA', NOW() - INTERVAL '10 days'),
('free', 'user005', 'IL', NOW() - INTERVAL '5 days'),
('free', 'user008', 'CA', NOW() - INTERVAL '12 days'),
('free', 'user010', 'PA', NOW() - INTERVAL '8 days'),
('free', 'user013', 'MI', NOW() - INTERVAL '15 days'),
('free', 'user017', 'NC', NOW() - INTERVAL '20 days'),
('free', 'user019', 'SC', NOW() - INTERVAL '7 days'),
('free', 'user022', 'NV', NOW() - INTERVAL '18 days'),
('free', 'user025', 'VA', NOW() - INTERVAL '9 days'),
('free', 'user028', 'CT', NOW() - INTERVAL '14 days'),

-- Some level upgrades
('free', 'user001', 'NY', NOW() - INTERVAL '60 days'),
('free', 'user007', 'NY', NOW() - INTERVAL '45 days'),
('paid', 'user001', 'NY', NOW() - INTERVAL '30 days'),
('paid', 'user007', 'NY', NOW() - INTERVAL '15 days');
